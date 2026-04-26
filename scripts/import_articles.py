"""
博客文章导入脚本

功能：
1. 读取格式化后的 Markdown 文档
2. 解析 YAML frontmatter 和文章内容
3. 创建分类和标签（如果不存在）
4. 导入文章到 MongoDB 数据库
"""

import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio
import re

# MongoDB 配置
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://admin:password@localhost:27017/?authSource=admin",
)
DATABASE_NAME = os.getenv("MONGODB_DB_NAME", "personal_blog")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change_me")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

# 目录配置
FORMATTED_DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "markdown-formatted")

# 默认作者 ID（需要先创建管理员账户）
DEFAULT_AUTHOR_ID = None  # 稍后设置


class BlogImporter:
    def __init__(self, mongodb_url: str, database_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[database_name]
        self.categories_cache = {}  # {name: ObjectId}
        self.tags_cache = {}  # {name: ObjectId}

    async def init_author(self) -> ObjectId:
        """初始化默认管理员账户"""
        admin_user = await self.db.users.find_one({"username": ADMIN_USERNAME})

        if not admin_user:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            admin_user = {
                "username": ADMIN_USERNAME,
                "email": ADMIN_EMAIL,
                "password_hash": pwd_context.hash(ADMIN_PASSWORD),
                "role": "admin",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = await self.db.users.insert_one(admin_user)
            admin_user["_id"] = result.inserted_id
            print(f"✅ 创建管理员账户: {ADMIN_USERNAME}")

        return admin_user["_id"]

    async def get_or_create_category(self, name: str, board: str = "tech") -> ObjectId:
        """获取或创建分类"""
        if name in self.categories_cache:
            return self.categories_cache[name]

        category = await self.db.categories.find_one({"name": name, "board": board})

        if not category:
            category = {
                "name": name,
                "board": board,
                "description": f"{name}相关的技术文章",
                "created_at": datetime.utcnow()
            }
            result = await self.db.categories.insert_one(category)
            category["_id"] = result.inserted_id
            print(f"  ✅ 创建分类: {name}")

        self.categories_cache[name] = category["_id"]
        return category["_id"]

    async def get_or_create_tag(self, name: str) -> ObjectId:
        """获取或创建标签"""
        if name in self.tags_cache:
            return self.tags_cache[name]

        tag = await self.db.tags.find_one({"name": name})

        if not tag:
            tag = {
                "name": name,
                "article_count": 0,
                "created_at": datetime.utcnow()
            }
            result = await self.db.tags.insert_one(tag)
            tag["_id"] = result.inserted_id
            print(f"  ✅ 创建标签: {name}")

        self.tags_cache[name] = tag["_id"]
        return tag["_id"]

    def parse_markdown_file(self, file_path: str) -> Optional[Dict]:
        """解析 Markdown 文件（包含 YAML frontmatter）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析 YAML frontmatter
            if not content.startswith('---'):
                print(f"  ⚠️ 文件缺少 frontmatter: {file_path}")
                return None

            # 分离 frontmatter 和正文
            parts = content.split('---', 2)
            if len(parts) < 3:
                print(f"  ⚠️ frontmatter 格式错误: {file_path}")
                return None

            frontmatter = yaml.safe_load(parts[1])
            markdown_content = parts[2].strip()

            return {
                "frontmatter": frontmatter,
                "content": markdown_content
            }

        except Exception as e:
            print(f"  ❌ 解析文件失败 {file_path}: {e}")
            return None

    def _parse_datetime(self, dt_value) -> datetime:
        """解析时间，支持字符串和datetime对象"""
        if dt_value is None:
            return datetime.utcnow()

        if isinstance(dt_value, datetime):
            return dt_value

        if isinstance(dt_value, str):
            try:
                return datetime.fromisoformat(dt_value.replace('Z', '+00:00'))
            except ValueError:
                return datetime.utcnow()

        return datetime.utcnow()

    async def import_article(self, file_path: str, author_id: ObjectId) -> bool:
        """导入单篇文章"""
        parsed = self.parse_markdown_file(file_path)
        if not parsed:
            return False

        frontmatter = parsed["frontmatter"]
        content = parsed["content"]

        # 获取或创建分类
        category_id = await self.get_or_create_category(
            frontmatter.get("category", "其他"),
            frontmatter.get("board", "tech")
        )

        # 获取或创建标签
        tag_names = frontmatter.get("tags", [])
        tag_ids = []
        for tag_name in tag_names:
            tag_id = await self.get_or_create_tag(tag_name)
            tag_ids.append(tag_id)

        # 检查文章是否已存在
        existing = await self.db.articles.find_one({
            "title": frontmatter.get("title"),
            "board": frontmatter.get("board", "tech")
        })

        if existing:
            print(f"  ⚠️ 文章已存在，跳过: {frontmatter.get('title')}")
            return False

        # 创建文章文档
        article = {
            "title": frontmatter.get("title", "未命名文章"),
            "content": content,
            "summary": frontmatter.get("summary", ""),
            "board": frontmatter.get("board", "tech"),
            "category_id": category_id,
            "tags": tag_names,  # 保存标签名称数组
            "author_id": author_id,
            "cover_image": frontmatter.get("cover_image", ""),
            "view_count": 0,
            "like_count": 0,
            "is_published": frontmatter.get("is_published", True),
            "created_at": self._parse_datetime(frontmatter.get("created_at")),
            "updated_at": self._parse_datetime(frontmatter.get("updated_at"))
        }

        # 插入文章
        result = await self.db.articles.insert_one(article)

        # 更新标签的文章计数
        for tag_name in tag_names:
            await self.db.tags.update_one(
                {"name": tag_name},
                {"$inc": {"article_count": 1}}
            )

        print(f"  ✅ 导入文章: {article['title']}")
        return True

    async def import_all_articles(self, docs_dir: str):
        """批量导入所有文章"""
        print("\n" + "="*80)
        print("开始导入文章到数据库")
        print("="*80 + "\n")

        # 初始化管理员账户
        print("1. 初始化管理员账户...")
        author_id = await self.init_author()

        # 获取所有 Markdown 文件
        md_files = sorted(Path(docs_dir).glob("*.md"))
        print(f"\n2. 找到 {len(md_files)} 个文档\n")

        # 导入文章
        success_count = 0
        skip_count = 0
        error_count = 0

        for i, file_path in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] 处理: {file_path.name}")

            try:
                if await self.import_article(str(file_path), author_id):
                    success_count += 1
                else:
                    skip_count += 1
            except Exception as e:
                print(f"  ❌ 导入失败: {e}")
                error_count += 1

        # 统计信息
        print("\n" + "="*80)
        print("导入完成统计")
        print("="*80)
        print(f"✅ 成功导入: {success_count} 篇")
        print(f"⚠️ 跳过重复: {skip_count} 篇")
        print(f"❌ 导入失败: {error_count} 篇")
        print(f"📊 总计处理: {len(md_files)} 篇")

        # 数据库统计
        total_articles = await self.db.articles.count_documents({})
        total_categories = await self.db.categories.count_documents({})
        total_tags = await self.db.tags.count_documents({})

        print(f"\n数据库统计:")
        print(f"  文章总数: {total_articles}")
        print(f"  分类总数: {total_categories}")
        print(f"  标签总数: {total_tags}")
        print("="*80 + "\n")

    async def close(self):
        """关闭数据库连接"""
        self.client.close()


async def main():
    """主函数"""
    importer = BlogImporter(MONGODB_URL, DATABASE_NAME)

    try:
        await importer.import_all_articles(FORMATTED_DOCS_DIR)
    finally:
        await importer.close()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         博客文章导入工具 v1.0                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

功能说明:
  1. 自动创建管理员账户 (admin/admin123)
  2. 解析 Markdown 文件的 YAML frontmatter
  3. 自动创建分类和标签
  4. 导入文章到 MongoDB 数据库
  5. 更新标签文章计数

数据库配置:
  URL: {MONGODB_URL}
  数据库: {DATABASE_NAME}

文档目录: {FORMATTED_DOCS_DIR}

注意事项:
  - 请确保 MongoDB 服务已启动
  - 请确保已安装依赖: pip install motor pyyaml passlib[bcrypt]
  - 管理员默认密码为 admin123，导入后请立即修改
    """.format(
        MONGODB_URL=MONGODB_URL,
        DATABASE_NAME=DATABASE_NAME,
        FORMATTED_DOCS_DIR=FORMATTED_DOCS_DIR
    ))

    # input("按回车键开始导入...")

    asyncio.run(main())
