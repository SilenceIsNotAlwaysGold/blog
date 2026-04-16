import { onMounted, onUnmounted, type Ref } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export function useScrollReveal(
  containerRef: Ref<HTMLElement | null>,
  selector: string,
  options: {
    y?: number
    duration?: number
    stagger?: number
    delay?: number
  } = {}
) {
  const { y = 40, duration = 0.7, stagger = 0.12, delay = 0 } = options
  let ctx: gsap.Context | null = null

  onMounted(() => {
    if (!containerRef.value) return
    ctx = gsap.context(() => {
      gsap.from(selector, {
        y,
        opacity: 0,
        duration,
        stagger,
        delay,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: containerRef.value!,
          start: 'top 85%',
          once: true,
        },
      })
    }, containerRef.value)
  })

  onUnmounted(() => {
    ctx?.revert()
  })
}
