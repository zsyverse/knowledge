// 用法：node scripts/check_katex.js file1.md [file2.md ...]
// 抽取 Markdown 中的 $$...$$ 与 $...$ 公式（跳过代码块），用站点同一套宏渲染，报告解析错误。
const fs = require("fs")
const path = require("path")
const katex = require(path.join(__dirname, "../docs/assets/vendor/katex/katex.min.js"))
const src = fs.readFileSync(path.join(__dirname, "../docs/assets/javascripts/katex.js"), "utf8")
const KATEX_MACROS = eval("(" + src.match(/const KATEX_MACROS = (\{[\s\S]*?\n\})/)[1] + ")")
let bad = 0, total = 0
for (const file of process.argv.slice(2)) {
  let text = fs.readFileSync(file, "utf8")
  text = text.replace(/^( *)(```|~~~)[\s\S]*?^\1\2/gm, "").replace(/`[^`\n]*`/g, "")
  const items = []
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, m) => { items.push([m, true]); return " " })
  text.replace(/(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$/g, (_, m) => { items.push([m, false]); return " " })
  for (const [tex, display] of items) {
    total++
    try { katex.renderToString(tex, { displayMode: display, throwOnError: true, macros: { ...KATEX_MACROS } }) }
    catch (e) { bad++; console.log(`${file}: ${e.message.split("\n")[0]}\n    ${tex.trim().slice(0, 160)}`) }
  }
}
console.log(`checked ${total} formulas, ${bad} errors`)
process.exit(bad ? 1 : 0)
