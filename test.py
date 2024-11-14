.video-container {
    display: flex; /* 使用Flexbox布局 */
    overflow-x: auto; /* 允许水平滚动 */
    gap: 10px; /* 设置视频之间的间隙为0 */
}

.video-item {
    flex: 0 0 60%; /* 每个项目占据30%的宽度，并且不伸缩 */
}

.video-item video {
    width: 100%; /* 视据宽度占满父容器 */
    height: auto; /* 高度自适应 */
}


