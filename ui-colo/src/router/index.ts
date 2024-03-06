import { type RouteRecordRaw, createRouter } from "vue-router"
import { history, flatMultiLevelRoutes } from "./helper"
import routeSettings from "@/config/route"

const Layouts = () => import("@/layouts/index.vue")

/**
 * 常驻路由
 * 除了 redirect/403/404/login 等隐藏页面，其他页面建议设置 Name 属性
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    component: Layouts,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue")
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error-page/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error-page/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/",
    component: Layouts,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        name: "Dashboard",
        meta: {
          title: "首页",
          svgIcon: "dashboard",
          affix: true
        }
      }
    ]
  },
  {
    path: "/user",
    component: Layouts,
    redirect: "/user",
    name: "User",
    meta: {
      title: "用户管理",
      elIcon: "Grid"
    },
    children: [
      {
        path: "user",
        component: () => import("@/views/menu/menu2/index.vue"),
        name: "plan",
        meta: {
          title: "用户管理",
          svgIcon: "component",
          keepAlive: true
        }
      },
    ]
  },
  {
    path: "/perf",
    component: Layouts,
    redirect: "/perf/plan",
    name: "Perf",
    meta: {
      title: "性能测试",
      elIcon: "Grid"
    },
    children: [
       {
        path: "script",
        component: () => import("@/views/perf/script.vue"),
        name: "Script",
        meta: {
          title: "脚本管理", // 脚本上传，脚本调试，脚本运行
          keepAlive: true
        }
      },
      {
        path: "plan",
        component: () => import("@/views/perf/plan.vue"),
        name: "Plan",
        meta: {
          title: "测试计划",
          keepAlive: true
        }
      },
      {
        path: "testRecord",
        component: () => import("@/views/perf/testRecord.vue"),
        name: "TestRecord",
        meta: {
          title: "测试记录",
          keepAlive: false
        }
      }
    ]
  },
  {
    path: "/env",
    component: Layouts,
    redirect: "/env",
    name: "",
    meta: {
      title: "环境管理",
      elIcon: "Grid"
    },
    children: [
      {
        path: "env",
        component: () => import("@/views/test-machine/index.vue"),
        name: "Env",
        meta: {
          title: "环境管理",
          svgIcon: "menu",
          keepAlive: true
        }
      },
    ]
  },
  {
    path: "/system",
    component: Layouts,
    redirect: "/system",
    name: "System",
    meta: {
      title: "系统管理",
      elIcon: "system"
    },
    children: [
      {
        path: "system",
        component: () => import("@/views/menu/menu2/index.vue"),
        name: "System",
        meta: {
          title: "系统配置",
          svgIcon: "unocss",
          keepAlive: true
        }
      },
    ]
  },
  // {
  //   path: "/menu",
  //   component: Layouts,
  //   redirect: "/menu/menu1",
  //   name: "Menu",
  //   meta: {
  //     title: "多级路由",
  //     svgIcon: "menu"
  //   },
  //   children: [
  //     {
  //       path: "menu1",
  //       component: () => import("@/views/menu/menu1/plan.vue"),
  //       redirect: "/menu/menu1/menu1-1",
  //       name: "Menu1",
  //       meta: {
  //         title: "menu1"
  //       },
  //       children: [
  //         {
  //           path: "menu1-1",
  //           component: () => import("@/views/menu/menu1/menu1-1/plan.vue"),
  //           name: "Menu1-1",
  //           meta: {
  //             title: "menu1-1",
  //             keepAlive: true
  //           }
  //         },
  //         {
  //           path: "menu1-2",
  //           component: () => import("@/views/menu/menu1/menu1-2/plan.vue"),
  //           redirect: "/menu/menu1/menu1-2/menu1-2-1",
  //           name: "Menu1-2",
  //           meta: {
  //             title: "menu1-2"
  //           },
  //           children: [
  //             {
  //               path: "menu1-2-1",
  //               component: () => import("@/views/menu/menu1/menu1-2/menu1-2-1/plan.vue"),
  //               name: "Menu1-2-1",
  //               meta: {
  //                 title: "menu1-2-1",
  //                 keepAlive: true
  //               }
  //             },
  //             {
  //               path: "menu1-2-2",
  //               component: () => import("@/views/menu/menu1/menu1-2/menu1-2-2/plan.vue"),
  //               name: "Menu1-2-2",
  //               meta: {
  //                 title: "menu1-2-2",
  //                 keepAlive: true
  //               }
  //             }
  //           ]
  //         },
  //         {
  //           path: "menu1-3",
  //           component: () => import("@/views/menu/menu1/menu1-3/plan.vue"),
  //           name: "Menu1-3",
  //           meta: {
  //             title: "menu1-3",
  //             keepAlive: true
  //           }
  //         }
  //       ]
  //     },
  //     {
  //       path: "menu2",
  //       component: () => import("@/views/menu/menu2/plan.vue"),
  //       name: "Menu2",
  //       meta: {
  //         title: "menu2",
  //         keepAlive: true
  //       }
  //     }
  //   ]
  // },
]

/**
 * 动态路由
 * 用来放置有权限 (Roles 属性) 的路由
 * 必须带有 Name 属性
 */
export const asyncRoutes: RouteRecordRaw[] = [
  {
    path: "/permission",
    component: Layouts,
    redirect: "/permission/page",
    name: "Permission",
    meta: {
      title: "权限管理",
      svgIcon: "lock",
      roles: ["admin", "editor"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "page",
        component: () => import("@/views/permission/page.vue"),
        name: "PagePermission",
        meta: {
          title: "页面权限",
          roles: ["admin"] // 或者在子导航中设置角色
        }
      },
      {
        path: "directive",
        component: () => import("@/views/permission/directive.vue"),
        name: "DirectivePermission",
        meta: {
          title: "指令权限" // 如果未设置角色，则表示：该页面不需要权限，但会继承根路由的角色
        }
      }
    ]
  },
  {
    path: "/:pathMatch(.*)*", // Must put the 'ErrorPage' route at the end, 必须将 'ErrorPage' 路由放在最后
    redirect: "/404",
    name: "ErrorPage",
    meta: {
      hidden: true
    }
  }
]

const router = createRouter({
  history,
  routes: routeSettings.thirdLevelRouteCache ? flatMultiLevelRoutes(constantRoutes) : constantRoutes
})

/** 重置路由 */
export function resetRouter() {
  // 注意：所有动态路由路由必须带有 Name 属性，否则可能会不能完全重置干净
  try {
    router.getRoutes().forEach((route) => {
      const { name, meta } = route
      if (name && meta.roles?.length) {
        router.hasRoute(name) && router.removeRoute(name)
      }
    })
  } catch {
    // 强制刷新浏览器也行，只是交互体验不是很好
    window.location.reload()
  }
}

export default router
