import { getInfoApi, loginApi, logoutApi, registerApi } from "@/api/user";
import { resetRouter } from "@/router";
import { getToken, removeToken, setToken } from "@/utils/auth";

const state = {
  token: getToken(),
  name: "",
  email: "",
  avatar: "",
  roles: [],
};

const mutations = {
  //token
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  //用户名
  SET_NAME: (state, name) => {
    state.name = name;
  },
  //邮箱
  SET_EMAIL: (state, email) => {
    state.email = email;
  },
  //头像
  SET_AVATAR: (state, avatar) => {
    state.avatar =
      avatar ??
      "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png";
  },
  //角色，用于权鉴
  SET_ROLES: (state, roles) => {
    state.roles = roles;
  },
};

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo;
    return new Promise((resolve, reject) => {
      loginApi({ username: username.trim(), password: password })
        .then((response) => {
          const { data } = response;
          commit("SET_TOKEN", data.token);
          setToken(data.token);

          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // 注册
  register({ commit }, userInfo) {
    const { username, email, password } = userInfo;
    return new Promise((resolve, reject) => {
      registerApi({
        username: username.trim(),
        email: email,
        password: password,
      })
        .then((response) => {
          const { data } = response;
          commit("SET_TOKEN", data.token);
          setToken(data.token);

          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // 获取用户信息
  getInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfoApi()
        .then((response) => {
          const { data } = response;

          if (!data) {
            reject("验证失败，请再次登录。");
          }

          const { roles, name, email, avatar } = data;

          // 角色必须是非空数组
          if (!roles || roles.length <= 0) {
            reject("getInfo：角色必须是非空数组！");
          }

          commit("SET_ROLES", roles);
          commit("SET_NAME", name);
          commit("SET_EMAIL", email);
          commit("SET_AVATAR", avatar);

          resolve(data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // 用户注销
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logoutApi(state.token)
        .then(() => {
          commit("SET_TOKEN", "");
          commit("SET_ROLES", []);
          commit("SET_AVATAR", "");
          removeToken();
          resetRouter();

          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // 删除令牌
  resetToken({ commit }) {
    return new Promise((resolve) => {
      commit("SET_TOKEN", "");
      commit("SET_ROLES", []);
      removeToken();
      resolve();
    });
  },

  // 设置头像
  setAvatar({ commit }, avatar) {
    commit("SET_AVATAR", avatar);
  },

  // 设置用户名
  setName({ commit }, name) {
    commit("SET_NAME", name);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
