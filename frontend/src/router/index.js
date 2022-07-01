/* Layout */
import Layout from "@/layout";
import Login from "@/views/login";
import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export const constantRoutes = [
  {
    path: "/login",
    component: Login,
    hidden: true,
    meta: { title: "登录", icon: "edit" },
  },
  {
    path: "/register",
    component: () => import("@/views/register/index"),
    hidden: true,
    meta: { title: "注册", icon: "edit" },
  },
  {
    path: "/404",
    component: () => import("@/views/404"),
    hidden: true,
  },
  {
    path: "/",
    redirect: "/dashboard",
    component: Layout,
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/dashboard/index"),
        meta: { title: "主控台", icon: "dashboard" },
      },
    ],
  },
  {
    path: "/profile",
    component: Layout,
    children: [
      {
        path: "",
        component: () => import("@/views/profile/index"),
        name: "Profile",
        meta: { title: "个人中心", icon: "user", noCache: true },
      },
    ],
  },
  {
    path: "/myDataset",
    component: Layout,
    children: [
      {
        path: "",
        component: () => import("@/views/myDatasetList/index"),
        name: "myDataset",
        meta: {
          title: "个人数据集",
          icon: "el-icon-document-copy",
          noCache: true,
        },
      },
    ],
  },
  {
    path: "/imageAnnotate",
    component: Layout,
    hidden: true,
    children: [
      {
        path: ":id",
        component: () => import("@/views/imageAnnotate/index"),
        name: "Annotate",
        meta: { title: "标注界面", icon: "edit", noCache: true },
      },
    ],
  },
  {
    path: "/datasetCommunity",
    component: Layout,
    children: [
      {
        path: "",
        component: () => import("@/views/community/index"),
        name: "Community",
        meta: {
          title: "数据集社区",
          icon: "el-icon-office-building",
          noCache: true,
        },
      },
    ],
  },
  {
    path: "/labelsManage",
    component: Layout,
    children: [
      {
        path: "",
        name: "labelsManage",
        component: () => import("@/views/labelsManage"),
        meta: { title: "标签管理", icon: "el-icon-setting" },
      },
    ],
  },
  {
    path: "/groupManage",
    component: Layout,
    redirect: "index",
    children: [
      {
        path: "",
        component: () => import("@/views/groupManage/index"),
        name: "Group",
        meta: { title: "成员管理", icon: "group", noCache: true },
      },
    ],
  },

  { path: "*", redirect: "/404", hidden: true },
];

const createRouter = () =>
  new Router({
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRoutes,
    mode: "history",
  });

const router = createRouter();

export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher;
}

export default router;
