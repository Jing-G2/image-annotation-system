<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">
        <el-col :span="8" :xs="24">
          <UserCard :user="user" />
        </el-col>
        <el-col :span="16" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="账号信息" name="account">
                <Account :user="user" />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import UserCard from "./components/UserCard";
import Account from "./components/Account";

export default {
  name: "Profile",
  components: { UserCard,  Account },
  data() {
    return {
      user: {},
      activeTab: "account",
    };
  },
  computed: {
    ...mapGetters(["name", "email"]),
  },
  created() {
    this.getUser();
  },
  methods: {
    getUser() {
      this.user = {
        name: this.name,
        email: this.email,
      };
    },
  },
};
</script>
