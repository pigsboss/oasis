# OASIS sky cubemap viewer

Standalone WebGL1 viewer for six-face true-colour cubemaps.

## Assets

The default face files are generated from the v4 CIE equirectangular map:

```text
/mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_v4/
  index.html
  px.jpg nx.jpg py.jpg ny.jpg pz.jpg nz.jpg
```

Regenerate:

```bash
python tools/equirect_to_cubemap.py \
  --equirect /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/gaia_dr3_v4_cie_equirect_8192x4096_reinhard.png \
  --out-dir /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_v4 \
  --size 2048
```

## Serve

Do not open `index.html` with `file://`; WebGL texture loading needs HTTP.

```bash
python3 -m http.server 8090 \
  --directory /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_v4
```

Open:

```text
http://<host>:8090/index.html
```

## Controls

- drag: rotate
- wheel / pinch: zoom
- double click / R: reset
- arrows: rotate; +/-: zoom
- 自动旋转: toggle autorotation
- 全屏: fullscreen

Faces use the standard OpenGL cube-map direction mapping, with
`UNPACK_FLIP_Y_WEBGL=true`.


## Email / single-file edition

For email, embed the six faces as base64 data URIs:

```bash
python tools/embed_cubemap_html.py \
  --template tools/skyviewer/index.html \
  --faces /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024 \
  --out /mnt/data/huo/Datasets/Gaia/gdr3/spectral/maps_cie/cubemap_email_1024/gaia_dr3_skyviewer_email.html
```

The result is a single 4.2 MB HTML file with no external URLs. Attach it as a
file; open the attachment in a normal browser. HTML email bodies usually block
JavaScript, so do not paste it into the message body.
