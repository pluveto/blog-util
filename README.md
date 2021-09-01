# blog util

一个博客发布接口。此程序能够收集散落各处的 Typora 标准的 Markdown 文件，对其进行预处理（如转义、格式规范化，使之在浏览器也能像 Typora 中一样正常显示）并将其按照一定规则（`file_list.yaml`）复制到 hugo 的源文件目录中，然后通过 hugo 发布。

使用方法：

1. 配置 `file_list.yaml`
2. 执行下列命令发布：
   ```bash
   py update.py
   ```