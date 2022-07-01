<template>
  <el-row :gutter="20">
    <el-col :xs="24" :sm="24" :lg="24">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>个人信息</span>
        </div>
        <div>
          <div style="text-align: center">
            <div class="el-upload">
              <el-upload
                class="avatar-uploader"
                :headers="{ 'annotate-system-token': token }"
                name="avatar"
                action="http://localhost:8000/api/setAvatar/"
                :show-file-list="false"
                accept="image/*"
                :on-success="handleSuccess"
                :on-error="handleError"
                ><img :src="avatar" class="avatar" alt="" />
              </el-upload>
            </div>
            <p style="font-size: 10px">点击图片更换头像</p>
          </div>
          <ul class="user-info">
            <li>
              <SvgIcon icon-class="user" /> 用户名
              <div class="user-right">
                {{ user.name }}
              </div>
            </li>
            <li>
              <SvgIcon icon-class="email" /> 邮箱
              <div class="user-right">
                {{ user.email }}
              </div>
            </li>

            <li>
              <SvgIcon icon-class="anq" /> 安全设置
              <div class="user-right">
                <el-button type="text" @click="dialogFormVisible = true">
                  修改密码
                </el-button>

                <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
                  <el-form
                    :model="pwdOptions"
                    ref="pwdOptions"
                    :rules="pwdRules"
                  >
                    <el-form-item
                      prop="oldPassword"
                      label="旧密码"
                      :label-width="formLabelWidth"
                    >
                      <el-input
                        show-password
                        v-model="pwdOptions.oldPassword"
                        placeholder="请输入旧密码"
                        autocomplete="off"
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="新密码"
                      :label-width="formLabelWidth"
                      prop="newPassword"
                    >
                      <el-input
                        show-password
                        v-model="pwdOptions.newPassword"
                        placeholder="请输入新密码"
                        autocomplete="off"
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="确认密码"
                      :label-width="formLabelWidth"
                      prop="checkPassword"
                    >
                      <el-input
                        show-password
                        v-model="pwdOptions.checkPassword"
                        placeholder="请再次确认"
                        autocomplete="off"
                      ></el-input>
                    </el-form-item>
                  </el-form>
                  <div class="dialog-footer">
                    <el-button type="primary" @click="handleUpdatePassword">
                      确 定
                    </el-button>
                    <el-button @click="dialogFormVisible = false">
                      取 消
                    </el-button>
                  </div>
                </el-dialog>
              </div>
            </li>
          </ul>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { userInfoUpdatePasswordApi } from "@/api/user.js";
import { validateRegisterPassword } from "@/utils/validate.js";
import { getToken } from "@/utils/auth";
import { mapGetters } from "vuex";
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: "",
          email: "",
        };
      },
    },
  },
  data() {
    return {
      dialogFormVisible: false,
      pwdOptions: {
        oldPassword: "",
        newPassword: "",
        checkPassword: "",
      },
      pwdRules: {
        oldPassword: [
          {
            required: true,
            trigger: "blur",
            validator: validateRegisterPassword,
          },
        ],
        newPassword: [
          {
            required: true,
            trigger: "blur",
            validator: validateRegisterPassword,
          },
        ],
        checkPassword: [
          {
            required: true,
            trigger: "blur",
            validator: validateRegisterPassword,
          },
        ],
      },
      formLabelWidth: "80px",
    };
  },
  computed: {
    token() {
      return getToken();
    },
    ...mapGetters(["avatar"]),
  },
  methods: {
    handleUpdatePassword() {
      this.$refs.pwdOptions.validate((valid) => {
        if (valid) {
          if (this.pwdOptions.newPassword != this.pwdOptions.checkPassword) {
            this.$message.error("两次输入的密码不一致，修改密码失败");
          } else {
            userInfoUpdatePasswordApi({
              oldPassword: this.pwdOptions.oldPassword,
              newPassword: this.pwdOptions.newPassword,
            }).then((res) => {
              this.$message({
                message: "用户密码更新成功",
                type: "success",
                duration: 5 * 1000,
              });
            });
          }
        } else {
          console.log("提交错误!!");
          return false;
        }
      });
    },
    handleSuccess(response) {
      this.$store.dispatch("user/setAvatar", response.data.avatar);
    },
    handleError() {
      this.$message.error("上传失败");
    },
  },
};
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.avatar {
  width: 150px;
  height: 150px;
}

.user-info {
  padding-left: 0;
  list-style: none;

  li {
    border-bottom: 1px solid #f0f3f4;
    padding: 11px 0;
    font-size: 13px;
  }

  .user-right {
    float: right;

    .dialog-footer {
      position: relative;
      left: 275px;
    }
  }
}
</style>
