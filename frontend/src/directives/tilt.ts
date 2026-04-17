import type { Directive } from 'vue'

interface TiltState {
  onMove: (e: MouseEvent) => void
  onLeave: () => void
  onEnter: () => void
}

const TILT_MAX = 10
const SCALE = 1.03

export const vTilt: Directive<HTMLElement & { _tilt?: TiltState }> = {
  mounted(el) {
    if (window.matchMedia('(hover: none)').matches) return

    const glow = document.createElement('div')
    glow.className = 'tilt-glow'
    glow.style.cssText = [
      'position:absolute',
      'inset:0',
      'pointer-events:none',
      'border-radius:inherit',
      'opacity:0',
      'transition:opacity 0.3s',
      'background:radial-gradient(circle at var(--x) var(--y), rgba(255,255,255,0.18), transparent 40%)',
      'mix-blend-mode:plus-lighter',
      'z-index:10',
    ].join(';')
    el.appendChild(glow)

    const prevPosition = getComputedStyle(el).position
    if (prevPosition === 'static') el.style.position = 'relative'
    el.style.transformStyle = 'preserve-3d'
    el.style.transition = 'transform 0.2s ease-out'
    el.style.willChange = 'transform'

    const onMove = (e: MouseEvent) => {
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      const cx = rect.width / 2
      const cy = rect.height / 2
      const rotX = ((cy - y) / cy) * TILT_MAX
      const rotY = ((x - cx) / cx) * TILT_MAX
      el.style.transform = `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${SCALE})`
      glow.style.setProperty('--x', `${x}px`)
      glow.style.setProperty('--y', `${y}px`)
    }

    const onEnter = () => {
      glow.style.opacity = '1'
      el.style.transition = 'transform 0.1s ease-out'
    }

    const onLeave = () => {
      el.style.transition = 'transform 0.5s cubic-bezier(0.22, 1, 0.36, 1)'
      el.style.transform = 'perspective(900px) rotateX(0) rotateY(0) scale(1)'
      glow.style.opacity = '0'
    }

    el.addEventListener('mousemove', onMove)
    el.addEventListener('mouseenter', onEnter)
    el.addEventListener('mouseleave', onLeave)
    el._tilt = { onMove, onLeave, onEnter }
  },

  unmounted(el) {
    if (!el._tilt) return
    el.removeEventListener('mousemove', el._tilt.onMove)
    el.removeEventListener('mouseenter', el._tilt.onEnter)
    el.removeEventListener('mouseleave', el._tilt.onLeave)
    delete el._tilt
  },
}
