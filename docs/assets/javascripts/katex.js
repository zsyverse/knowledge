// 全站公共宏（与现代控制理论讲义的 LaTeX 宏一致）
const KATEX_MACROS = {
  "\\tp": "^{\\mathsf T}",
  "\\e": "\\mathrm{e}",
  "\\dd": "\\,\\mathrm{d}",
  "\\Lap": "\\mathcal{L}",
  "\\Zt": "\\mathcal{Z}",
  "\\R": "\\mathbb{R}",
  "\\bmat": "\\begin{bmatrix}#1\\end{bmatrix}",
  "\\smat": "\\left[\\begin{smallmatrix}#1\\end{smallmatrix}\\right]",
  "\\rank": "\\operatorname{rank}",
  "\\diag": "\\operatorname{diag}",
  "\\adj": "\\operatorname{adj}",
  "\\tr": "\\operatorname{tr}",
  "\\Ker": "\\operatorname{Ker}",
  "\\Ima": "\\operatorname{Im}",
}

// 块公式：直接渲染 div.arithmatex（避免分隔符外的换行被渲染成空行）
// 行内公式：交给 auto-render 处理 \( \)
document$.subscribe(({ body }) => {
  body.querySelectorAll("div.arithmatex").forEach((el) => {
    const tex = el.textContent.trim().replace(/^\\\[/, "").replace(/\\\]$/, "")
    try {
      katex.render(tex, el, { displayMode: true, throwOnError: false, macros: KATEX_MACROS })
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
    macros: KATEX_MACROS,
  })
})
