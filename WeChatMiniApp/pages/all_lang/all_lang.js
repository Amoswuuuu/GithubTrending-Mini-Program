var url = "http://192.168.2.40:9986/";
var page =0;
var page_size = 20;
var sort = "last";
var is_easy = 0;
var lange_id = 0;
var pos_id = 0;
var unlearn = 0;
 
  
// 获取数据的方法，具体怎么获取列表数据大家自行发挥
var GetList = function(that){
  that.setData({
    hidden:false
  });
  wx.request({
    url:url + 'all',
    success:function(res){
      console.info(res.data);
      // var list = that.data;
      // for(var i = 0; i < res.data.length; i++){
      //   list.push(res.data[i]);
      // }
      that.setData({
        list : res.data
      });
      page ++;
      that.setData({
        hidden:true
      });
    }
  });
}
Page({
 data:{
  hidden:true,
  list:[],
  scrollTop : 0,
  scrollHeight:0
 },
 onLoad:function(){
  //  这里要非常注意，微信的scroll-view必须要设置高度才能监听滚动事件，所以，需要在页面的onLoad事件中给scroll-view的高度赋值
   var that = this;
   wx.getSystemInfo({
     success:function(res){
       console.info(res.windowHeight);
       that.setData({
         scrollHeight:res.windowHeight
       });
     }
   });
 },
 onShow:function(){
  //  在页面展示之后先获取一次数据
  var that = this;
  GetList(that);
 },
 bindDownLoad:function(){
  //  该方法绑定了页面滑动到底部的事件
   var that = this;
   GetList(that);
 },
 scroll:function(event){
  //  该方法绑定了页面滚动时的事件，我这里记录了当前的position.y的值,为了请求数据之后把页面定位到这里来。
   this.setData({
     scrollTop : event.detail.scrollTop
   });
 },
 cellTap(e){
  console.log('click')
  console.log(e.currentTarget.dataset.link)
  const link = e.currentTarget.dataset.link
  wx.navigateTo({
    url: '../detail/detail?link=' + link,
    success: function(res){
      // success
    },
    fail: function(res) {
      // fail
    },
    complete: function(res) {
      // complete
    }
  })
 },
 refresh:function(event){
  //  该方法绑定了页面滑动到顶部的事件，然后做上拉刷新
   page = 0;
   this.setData({
     list : [],
     scrollTop : 0
   });
   GetList(this)
 }
})
