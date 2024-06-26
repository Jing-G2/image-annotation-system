(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
  ["chunk-761ef5a3"],
  {
    "622d": function (t, a, s) {
      "use strict";
      s("cff6");
    },
    9406: function (t, a, s) {
      "use strict";
      s.r(a);
      var e = function () {
          var t = this,
            a = t.$createElement,
            s = t._self._c || a;
          return s(
            "div",
            { staticClass: "dashboard-container" },
            [
              s(
                "el-row",
                { attrs: { gutter: 20 } },
                [
                  s(
                    "el-col",
                    { attrs: { xs: 24, sm: 12, lg: 6 } },
                    [
                      s(
                        "el-card",
                        {
                          staticClass: "mgb20",
                          staticStyle: { height: "252px" },
                          attrs: { shadow: "hover" },
                        },
                        [
                          s("div", { staticClass: "user-info" }, [
                            s(
                              "div",
                              { staticClass: "el-upload" },
                              [
                                s(
                                  "el-upload",
                                  {
                                    staticClass: "avatar-uploader",
                                    attrs: {
                                      headers: {
                                        "annotate-system-token": t.token,
                                      },
                                      name: "avatar",
                                      action:
                                        "http://localhost:8000/api/setAvatar/",
                                      "show-file-list": !1,
                                      accept: "image/*",
                                      "on-success": t.handleSuccess,
                                      "on-error": t.handleError,
                                    },
                                  },
                                  [
                                    s("img", {
                                      staticClass: "avatar",
                                      attrs: { src: t.avatar, alt: "" },
                                    }),
                                  ]
                                ),
                              ],
                              1
                            ),
                            s("div", { staticClass: "user-info-cont" }, [
                              s("div", { staticClass: "user-info-name" }, [
                                t._v(" " + t._s(t.name) + " "),
                              ]),
                            ]),
                          ]),
                          s("div", { staticClass: "user-info-list" }, [
                            t._v(" 角色： "),
                            s("span", [t._v(t._s(t.roles[0]))]),
                          ]),
                        ]
                      ),
                      s("el-card", [
                        s("h1", [t._v("使用说明")]),
                        s("h3", [t._v("接口尚未完善,凑合着用")]),
                        s("ol", [
                          s("li", [t._v("设置标注标签")]),
                          s("li", [
                            t._v(" 导入标注文本数据 "),
                            s("ul", [
                              s("li", [
                                t._v(
                                  "编码为utf-8(后期会改为任意编码),文件格式为 .txt文件"
                                ),
                              ]),
                              s("li", [
                                t._v(
                                  " 为了方便演示,把文件的每一行作为一个标注数据集,之后会加上把整个文本作为一个标注数据集 "
                                ),
                              ]),
                            ]),
                          ]),
                          s("li", [t._v("点击按钮开始标注")]),
                          s("li", [t._v("导出数据")]),
                        ]),
                      ]),
                    ],
                    1
                  ),
                  s(
                    "el-col",
                    { attrs: { xs: 24, sm: 12, lg: 12 } },
                    [s("TodoList")],
                    1
                  ),
                ],
                1
              ),
            ],
            1
          );
        },
        o = [],
        r = s("f3f3"),
        n = s("2f62"),
        i = s("5f87"),
        l = function () {
          var t = this,
            a = t.$createElement,
            s = t._self._c || a;
          return s(
            "div",
            [
              s(
                "el-card",
                { staticClass: "mgb20", attrs: { shadow: "hover" } },
                [
                  s("div", [s("h1", [t._v("TodoList")])]),
                  t._l(t.todos, function (a, e) {
                    return s("div", { key: e }, [
                      s("li", [t._v(" " + t._s(a) + " ")]),
                      s("hr"),
                    ]);
                  }),
                ],
                2
              ),
            ],
            1
          );
        },
        c = [],
        d = {
          name: "TodoList",
          data: function () {
            return {
              todos: [
                "修改标注标签的颜色值后,标注页对应已标注的词的背景颜色跟着改变",
                "标注未完成时添加标签会清空标注数据,可能需要使用id来进行一一对应的修改",
                "提供用户手册（使用说明）",
                "根据始末位置进行标注",
                "考虑如何添加成员",
                "用户退出网站时提醒保存数据",
                "完善相关接口",
                "替换掉项目中的bootstrap样式",
                "属性标注",
                "关系标注",
                "翻译",
              ],
            };
          },
        },
        u = d,
        v = s("0c7c"),
        f = Object(v["a"])(u, l, c, !1, null, null, null),
        h = f.exports,
        _ = {
          name: "Dashboard",
          components: { TodoList: h },
          computed: Object(r["a"])(
            {
              token: function () {
                return Object(i["a"])();
              },
            },
            Object(n["b"])(["name", "avatar", "roles"])
          ),
          methods: {
            handleSuccess: function (t) {
              this.$store.dispatch("user/setAvatar", t.data.avatar);
            },
            handleError: function () {
              this.$message.error("上传失败");
            },
          },
        },
        m = _,
        p = (s("622d"), Object(v["a"])(m, e, o, !1, null, "2a188fd4", null));
      a["default"] = p.exports;
    },
    cff6: function (t, a, s) {},
  },
]);
