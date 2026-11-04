// 块公式：直接渲染 div.arithmatex（避免分隔符外的换行被渲染成空行）
// 行内公式：交给 auto-render 处理 \( \)
document$.subscribe(({ body }) => {
  body.querySelectorAll("div.arithmatex").forEach((el) => {
    const tex = el.textContent.trim().replace(/^\\\[/, "").replace(/\\\]$/, "")
    try {
      katex.render(tex, el, { displayMode: true, throwOnError: false })
    } catch (e) {
      console.error(e)
    }
  })
  renderMathInElement(body, {
    delimiters: [
      { left: "\\(", right: "\\)", display: false },
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    ignoredClasses: ["katex"],
  })
})
