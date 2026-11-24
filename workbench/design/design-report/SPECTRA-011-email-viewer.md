# SPECTRA-011：可邮件发送的单文件 cubemap 查看器

- 日期：2026-11-24
- 输入：8192×4096 CIE 真彩色等距圆柱映射
- 面分辨率：1024×1024，六面 JPEG q=82
- 输出：单个自包含 HTML（base64 内嵌六面）
- 文件大小：约 4.2 MB

## 文件

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024/gaia_dr3_skyviewer_email.html
```

## 生成

```bash
python tools/equirect_to_cubemap.py \
  --equirect /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/gaia_dr3_v4_cie_equirect_8192x4096_reinhard.png \
  --out-dir /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024 \
  --size 1024 --quality 82

python tools/embed_cubemap_html.py \
  --template tools/skyviewer/index.html \
  --faces /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024 \
  --out /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024/gaia_dr3_skyviewer_email.html
```

## 邮件发送

- 作为**附件**发送，不要粘贴到邮件正文；
- 邮件客户端通常会在正文中禁用 JavaScript；
- 收件人下载附件后，用 Chrome/Edge/Firefox/Safari 打开；
- 文件无需网络，无外部 URL；
- 六面 cubemap 已在 HTML 内 base64 内嵌。

建议主题：

```text
Gaia DR3 全天空沉浸式查看器
```

建议正文：

```text
附件是单个 HTML 文件，下载后用浏览器打开即可。
拖动旋转，滚轮/双指缩放，双击复位。
```

## 验证

```text
HTTP/HTTPS 外部引用  0
data:image/jpeg;base64 图像 6 个
大小                 4.2 MB
JS 语法              node --check 通过
```

## 说明

- 1024 面是为邮件体积做的压缩；高分辨率离线版仍为 `cubemap_v4/` 的 2048 面；
- 若邮件网关限制 HTML 附件，可先压缩为 zip；
- 查看器是纯 WebGL1，无第三方库。
