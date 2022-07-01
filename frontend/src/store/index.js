import Vue from "vue";
import Vuex from "vuex";

import settings from "./modules/settings";
import getters from "./getters";
import app from "./modules/app";
import user from "./modules/user";
import community from "./modules/community";
import myDataset from "./modules/myDataset";
import annotation from "./modules/annotation";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    annotation,
    community,
    myDataset,
  },
  getters,
});

export default store;
