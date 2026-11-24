# SPECTRA-016：银道坐标全量 Reinhard 4096 cubemap

- 日期：2026-11-25
- 源：全量 Gaia（有 G）1,806,254,432 颗
- 坐标：银道坐标 l/b
- 等距圆柱：8192×4096，中心 l=0，b=0 正对银心
- Tone：Reinhard luminance + gamma 2.2
- Cubemap：6 × 4096×4096
- HTML：六面 base64 内嵌

## 产物

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_galactic/
  gaia_full_galactic_8192x4096_psf3_reinhard.png/jpg

/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_v4/galactic_4096/
  px.jpg nx.jpg py.jpg ny.jpg pz.jpg nz.jpg
  index.html        29.2 MB，六面内嵌
  index_external.html
```

## 方向约定

- 世界坐标：x=cos b cos l, y=sin b, z=cos b sin l
- 等距圆柱：左边缘 l=-180，中心 l=0，右边缘 +180
- Cubemap +X 面中心为 l=0,b=0
- Viewer 初始 yaw=-π/2，pitch=0，画面中心正对银心
- HUD 显示 l/b

## 查看

```text
http://192.168.18.7:8090/galactic_4096/index.html
```

## 说明

- 29.2 MB 适合网页/本地；邮件发送需要另做低分辨率版
- 全量目前只包含有 G 的 1,806,254,432 颗
- 5,455,339 个缺 G 源尚未叠加
