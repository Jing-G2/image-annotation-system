<template>
  <div class="login-container">
    <div class="LoginContainer">
      <h3 style="text-align: center; margin: 20px 20px">Register</h3>
      <el-form
        ref="registerForm"
        :model="registerForm"
        status-icon
        :rules="registerRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username" style="margin-top: 30px">
          <el-input
            v-model="registerForm.username"
            type="text"
            tabindex="1"
            placeholder="请输入用户名"
            autocomplete="on"
          />
        </el-form-item>

        <el-form-item prop="email" label="邮箱" style="margin-top: 30px">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱地址"
            autocomplete="on"
          />
        </el-form-item>

        <el-form-item
          label="密码"
          prop="password"
          style="margin: 30px 0 30px 0"
        >
          <el-input
            :key="passwordType"
            ref="password"
            v-model="registerForm.password"
            :type="passwordType"
            placeholder="请输入密码"
            autocomplete="on"
            @keyup.enter.native="handleRegister"
          />
          <span class="show-pwd" @click="showPwd">
            <SvgIcon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>

        <el-button
          type="primary"
          style="width: 150px; margin: auto 60px 10px"
          @click.native.prevent="handleRegister"
        >
          Submit
        </el-button>

        <router-link :to="{ path: '/login' }" style="width: 150px">
          <el-button type="primary" style="width: 150px"> Back </el-button>
        </router-link>
      </el-form>
    </div>
  </div>
</template>

<script>
import {
  validateRegisterUsername,
  validateRegisterPassword,
} from "@/utils/validate.js";

export default {
  name: "Register",

  data() {
    return {
      //表单数据
      registerForm: {
        username: "",
        email: "",
        password: "",
      },
      //表单验证
      registerRules: {
        username: [
          {
            required: true,
            trigger: "blur",
            validator: validateRegisterUsername,
          },
        ],
        email: [
          {
            required: true,
            type: "email",
            message: "请输入正确的邮箱格式",
            trigger: ["blur", "change"],
          },
        ],
        password: [
          {
            required: true,
            trigger: "blur",
            validator: validateRegisterPassword,
          },
        ],
      },
      loading: false,
      passwordType: "password",
      redirect: undefined,
    };
  },
  watch: {
    $route: {
      handler: function (route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true,
    },
  },
  methods: {
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },

    handleRegister() {
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/register", this.registerForm)
            .then(() => {
              this.$router.push({
                path: this.redirect || "/",
              });
              this.loading = false;
            })
            .catch(() => {
              this.loading = false;
            });
        } else {
          console.log("提交错误!!");
          return false;
        }
      });
    },
  },
};
</script>

<style scoped>
.line {
  text-align: center;
}
</style>

<style lang="scss" scoped>
$bg: #8c9eb6;
$light_gray: #fff;
$cursor: #fff;

.LoginContainer {
  background: rgba(23, 89, 109, 0.1);
  border-radius: 15px;
  background-clip: padding-box;
  margin: 180px auto;
  width: 600px;
  padding: 20px 40px 20px 40px;
  border: 2px solid #02294e;
  box-shadow: 0 0 25px #1b1b3d;
}

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.055);
    background: rgba(0, 0, 0, 0.219);
    border-radius: 5px;
    color: #222121;
  }
}
</style>

<style lang="scss" scoped>
$bg: #363c4e;
$dark_gray: #98a3a8;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
}

.show-pwd {
  position: absolute;
  right: 10px;
  top: 7px;
  font-size: 16px;
  color: $dark_gray;
  cursor: pointer;
  user-select: none;
}
</style>
