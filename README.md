# ICE2604 项目概述

## 运行

* clone 整个文件夹
* 在根目录运行 `npm install --no-fund`
* 在根目录运行 `npm run dev`
* 打开浏览器窗口预览结果

## 难点与解决

1. 挂载函数的异步问题

在 `mounted()` 挂载中，本意是先运行 `searchInfo()` 再运行 `searchId()`，但在前者中未来及向 `_id` 赋值就运行了后者。这可能是因为异步操作导致的问题。异步操作是非阻塞的，意味着它们会在后台执行，并且不会等待其完成而继续执行后续代码。

为了解决这个问题，可以使用回调函数、Promise 或 async/await 等方式来确保在 `searchInfo` 完成后再调用 `searchId`
* 使用 Promise 的示例代码
```js
function searchInfo(callback) {
  // 在异步操作完成后调用回调函数
  setTimeout(function() {
    const _id = "12345"; // 这里是赋值 _id 的逻辑
    callback(_id);
  }, 1000); // 模拟异步操作的延迟
}

function searchId() {
  searchInfo(function(_id) {
    console.log("searchId: " + _id);
  });
}

searchId();
```
在上述代码中，searchInfo 函数中使用了 setTimeout 来模拟异步操作，并在操作完成后调用了回调函数，并将 _id 作为参数传递给回调函数。然后，searchId 函数通过传递一个回调函数给 searchInfo 函数来获取 _id，并在回调函数中打印 _id。

* 使用 async/await 的示例代码
将 `mounted()` 声明为异步函数，同时将所有需要优先完成的函数（即需要上锁的函数）前也加上`await`声明
```js
async mounted {
  await this.getAuthorPapers(0, 50);
  this.chart = echarts.init(document.getElementById('chart'));
  this.setChart();
}
```
并进一步在声明的异步函数中返回 `Promise` 类型，即直接返回 `axios` 的请求结果
```js
async getAuthorPapers(_start, _end) {
            return axios.get('http://10.80.135.205:8080/api/v1/vis/author/papers', {
                params: {}
            })
                .then((response) => {})
                .catch((error) => {})
        },
```

2. 优化回流和重绘次数
[提高前端性能：回流与重绘的优化策略](https://juejin.cn/post/7281581471897387071)

## 功能与展示

1. 

## 一些细节

1. 接口返回格式的统一化，比如各种数据库中的`key`名称，比如搜索结果返回的数据类型
2. 

## 广告

```
1. 上半句和下半句都要有同样的字。比如说 Macbook 的「满载动力，满足你的一天。」和「一身轻，更举重若轻。」以及说照片的「照过的再多，照样轻松找到。 」
2. 用完全不对仗但字数相同还押韵的句式，比如说 Retina 屏的「每一像素颗粒，尽显澎湃动力。」和说 iMessage 的「想说的，亲手写。」
3. 幼童式的口语化，比如说 iPad 的「Retina 的大作，一款又一款。」和母亲节活动宣传的「让妈妈开心的礼物，开了又开。」
4. 各种反义词。比如说 iPad mini 的「小身型，大有身手。」和说耳机的「无线，无繁琐，只有妙不可言。」
```
1. 唯一的不同，是处处都不同。（大标题）
2. 一身轻，更举重若轻。（功能少）
3. 满载动力，满足你乱想的词。（服务器）
4. 搜不搜在你，准不准在我。
5. 你的下一个搜索引擎，何必是你的。（用户信息完全泄漏，搜索记录数据库可见。你的隐私，我说了算。）
6. 快，比慢更快。（搜索后时间较长）
7. 全新用户登录协议，只许协，不许议。（注册登录页面）
8. （压力测试）

## 代办

1. 在搜索结果页面也加入搜索框
2. 改变搜索文章的年份
3. 判断返回的状态码，区分登录状态
4. arxiv作者格式不同
    ![arxiv作者格式不同](todo-author_format.png)
5. gpt交互
6. 主页面的可视化（按年份展示论文数、按作者展示论文数、（arxiv中按领域展示论文数））