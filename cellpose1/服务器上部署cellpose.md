cellpose使用流程简明总结

一、环境与安装
1. 创建虚拟环境，pip install cellpose
2. 本地下载cpsam（huggingface下载不可用），下载后CellposeModel会自动识别
3. 从github下载cellpose源码到服务器，解压。推荐用notebook中的案例学习。注意cellpose3的denoise模型（CPnet未定义不可用），cellpose-SAM可用
4. 推荐顺序：先test，后run，最后train

二、基本用法
- 初始化模型
  model = models.CellposeModel(gpu=True)
- 推理分割
  masks_pred, flows, styles = model.eval(imgs, niter=1000)
  imgs为图片列表，每个元素为三维（n,w,h），若为灰度图需手动拼成n=2的三维数组

三、结果可视化
- test结果可用如下方式画轮廓
  outlines_pred = utils.outlines_list(masks_pred[iex])
  for o in outlines_pred:
      plt.plot(o[:,0], o[:,1], color=[1,1,0.3], lw=0.75, ls="--")
  plt.axis('off')

- run批量推理
  dir = "./pos6/"  # 当前目录，文件需与py文件同目录
  files为图片列表，每个元素2*2048*2048
  masks, flows, styles = model.eval(files, batch_size=32, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, normalize={"tile_norm_blocksize": tile_norm_blocksize})

- 画图示例
  import numpy as np
  import matplotlib.pyplot as plt
  from cellpose import transforms, plot, utils, io
  plt.figure()
  for iex, img in enumerate(files):
      img = img.squeeze().copy()
      img = np.clip(transforms.normalize_img(img, axis=0), 0, 1)
      ax = plt.subplot(3, 3, iex+1)
      if img[1].sum() == 0:
          ax.imshow(img[0], cmap="gray")
      else:
          rgb = np.concatenate((np.zeros_like(img)[:1], img), axis=0).transpose(1,2,0)
          ax.imshow(rgb)
      ax.set_ylim([0, min(400, img.shape[0])])
      ax.set_xlim([0, min(400, img.shape[1])])
      outlines_pred = utils.outlines_list(masks[iex])
      for o in outlines_pred:
          plt.plot(o[:,0], o[:,1], color=[1,1,0.3], lw=0.75, ls="--")
      plt.axis('off')
  plt.tight_layout()
  plt.show()

四、eval参数简要说明
- x：输入图片（2D/3D/4D，需3通道）
- batch_size：批处理大小，影响显存
- resample：是否原图尺寸运行动力学，慢但更准
- channel_axis/z_axis：通道轴/Z轴，None自动判断
- normalize：归一化，可为True或dict（如tile_norm_blocksize等参数）
- invert：是否反转像素
- rescale/diameter：缩放因子/细胞直径
- flow_threshold/cellprob_threshold：流误差/细胞概率阈值
- do_3D/anisotropy/flow3D_smooth：3D相关参数
- stitch_threshold：3D拼接阈值
- min_size/max_size_fraction：掩码最小/最大尺寸
- niter：动力学迭代次数
- augment：数据增强
- tile_overlap/bsize：瓦片重叠/块大小
- compute_masks：是否返回掩码
- progress：进度条

五、输出说明
masks, flows, styles = model.eval(files, batch_size=32, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, normalize={"tile_norm_blocksize": tile_norm_blocksize})

masks为掩码，shape与files[0]一致，元素为0/1/2/...，0为背景，1、2...为不同细胞区域

待办：
模型微调构建数据集：先使用cellpose得到掩码，然后修改掩码