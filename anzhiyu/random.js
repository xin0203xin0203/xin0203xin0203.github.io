var posts=["posts/5023fd11.html","posts/ec54ee2f.html","posts/e1fbbea6.html","posts/924eec38.html","posts/dc6661ea.html","posts/1ec96998.html","posts/da145f53.html","posts/5a2ba262.html","posts/682fb25a.html","posts/e3a54e89.html","posts/9dacd182.html","posts/ff0c941c.html","posts/28f6f62f.html","posts/e170afa6.html","posts/1a829385.html","posts/1c48292.html","posts/411e35e9.html","posts/115d586a.html","posts/3cc2c9ad.html","posts/dd96b61.html","posts/1d7b1dd3.html","posts/e593d1c2.html","posts/e7ef9c46.html","posts/6e1f6090.html","posts/7355e8ed.html","posts/9a48b9a4.html","posts/188aa76e.html","posts/8fa701cd.html","posts/4a17b156.html","posts/9b7e4913.html"];function toRandomPost(){pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);};var friend_link_list=[{"name":"安知鱼`Blog","link":"https://blog.anheyu.com/","avatar":"https://npm.elemecdn.com/anzhiyu-blog-static@1.0.4/img/avatar.jpg","descr":"生活明朗，万物可爱","siteshot":"https://npm.elemecdn.com/anzhiyu-theme-static@1.1.6/img/blog.anheyu.com.jpg"},{"name":"Akilar","link":"https://akilar.top","avatar":"/img/siteicon/favicon.png","descr":"欢迎光临糖果屋"},{"name":"🌸さくら荘 の 一只二刺猿","link":"https://codeanime.cc/","avatar":"https://che.codeanime.xyz/images/2021/09/14/chimian.jpg","descr":"Codeanime","siteshot":null},{"name":"adguy","link":"https://adguy.top/","avatar":"https://adguycn990-typoraimage.oss-cn-hangzhou.aliyuncs.com/202211231910960.webp","descr":"十年饮冰，难凉热血"},{"name":"梦念逍遥のBLOG","link":"https://blog.lwtxiaoyao.top/","avatar":"https://cdn.staticaly.com/gh/MengNianxiaoyao/blogimages@main/siteicon/icon.png","descr":"无梦之境","siteshot":"https://cdn.staticaly.com/gh/MengNianxiaoyao/blogimages@main/siteicon/lwtxiaoyao.top.png"},{"name":"神经蛙","link":"https://hexo.sjava.cn/","avatar":"https://hexo.sjava.cn/img/pic.png","descr":"种一棵树最好的时间是十年前，其次是现在。","siteshot":"https://hexo.sjava.cn/img/sjw.png"},{"name":"贰猹的小窝","link":"https://noionion.top/","avatar":"https://pub-noionion.oss-cn-hangzhou.aliyuncs.com/head.jpg","descr":"用这生命中的每一秒，给自己一个不后悔的未来","siteshot":"https://pub-noionion.oss-cn-hangzhou.aliyuncs.com/noionion.top.png"},{"name":"AnFrank","link":"https://enfangzhong.github.io/","avatar":"https://enfangzhong.github.io/images/avatar.jpg","descr":"既可以早九晚五又可以浪迹天涯。"},{"name":"如鱼饮水，冷暖自知","link":"https://wangjiezhe.com","avatar":"https://wangjiezhe.com/images/avatar.jpg","descr":"蓝田生美玉，西风栽冷香。"},{"name":"张洪Heo","link":"https://blog.zhheo.com/","avatar":"https://bu.dusays.com/2022/12/28/63ac2812183aa.png","descr":"分享设计与科技生活"},{"name":"Eurkon","link":"https://blog.eurkon.com","avatar":"https://blog.eurkon.com/images/user/avatar.jpg","descr":"及时当勉励，岁月不待人。"},{"name":"Hexo","link":"https://hexo.io/zh-tw/","avatar":"https://d33wubrfki0l68.cloudfront.net/6657ba50e702d84afb32fe846bed54fba1a77add/827ae/logo.svg","descr":"快速、简单且强大网志框架"},{"name":"node.js","link":"https://nodejs.org/","avatar":"https://img.nodejs.cn/logo.svg","descr":"一个开源的跨平台 JavaScript 运行时环境"},{"name":"Youtube","link":"https://www.youtube.com/","avatar":"https://i.loli.net/2020/05/14/9ZkGg8v3azHJfM1.png","descr":"视频网站"},{"name":"Weibo","link":"https://www.weibo.com/","avatar":"https://i.loli.net/2020/05/14/TLJBum386vcnI1P.png","descr":"中国最大社交分享平台"},{"name":"Twitter","link":"https://twitter.com/","avatar":"https://i.loli.net/2020/05/14/5VyHPQqR6LWF39a.png","descr":"社交分享平台"}];
    var refreshNum = 1;
    function friendChainRandomTransmission() {
      const randomIndex = Math.floor(Math.random() * friend_link_list.length);
      const { name, link } = friend_link_list.splice(randomIndex, 1)[0];
      Snackbar.show({
        text:
          "点击前往按钮进入随机一个友链，不保证跳转网站的安全性和可用性。本次随机到的是本站友链：「" + name + "」",
        duration: 8000,
        pos: "top-center",
        actionText: "前往",
        onActionClick: function (element) {
          element.style.opacity = 0;
          window.open(link, "_blank");
        },
      });
    }
    function addFriendLinksInFooter() {
      var footerRandomFriendsBtn = document.getElementById("footer-random-friends-btn");
      if(!footerRandomFriendsBtn) return;
      footerRandomFriendsBtn.style.opacity = "0.2";
      footerRandomFriendsBtn.style.transitionDuration = "0.3s";
      footerRandomFriendsBtn.style.transform = "rotate(" + 360 * refreshNum++ + "deg)";
      const finalLinkList = [];
  
      let count = 0;

      while (friend_link_list.length && count < 3) {
        const randomIndex = Math.floor(Math.random() * friend_link_list.length);
        const { name, link, avatar } = friend_link_list.splice(randomIndex, 1)[0];
  
        finalLinkList.push({
          name,
          link,
          avatar,
        });
        count++;
      }
  
      let html = finalLinkList
        .map(({ name, link }) => {
          const returnInfo = "<a class='footer-item' href='" + link + "' target='_blank' rel='noopener nofollow'>" + name + "</a>"
          return returnInfo;
        })
        .join("");
  
      html += "<a class='footer-item' href='/link/'>更多</a>";

      document.getElementById("friend-links-in-footer").innerHTML = html;

      setTimeout(()=>{
        footerRandomFriendsBtn.style.opacity = "1";
      }, 300)
    };