<!--
程序名：网站登录页面
功能：进入网站的入口
-->
<template>
  <div class="login">
    <div class="main_login">
      <div class="title">登 录</div>
      <el-row type="flex" justify="center">
        <!-- 登录表单 -->
        <el-form ref="loginForm" :rules="rules" :model="loginForm">
            <el-form-item prop="username">
                <el-input @keyup.enter.native="login('loginForm')" icon="el-icon-search" placeholder="请输入用户名" v-model="loginForm.username">
                  <i class="el-icon-user" slot="prefix"> </i>
                </el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input @keyup.enter.native="login('loginForm')" placeholder="请输入密码" v-model="loginForm.password" show-password>
                  <i class="el-icon-lock" slot="prefix"> </i>
                </el-input>
            </el-form-item>
              <!-- 随机验证码 -->
            <el-form-item prop="verifycode" style="line-height:0px;">
              <el-input v-model="loginForm.verifycode" ref="verifycode" placeholder="验证码" class="identifyinput" style="width:250px;">
                <i class="el-icon-edit" slot="prefix"> </i>
              </el-input>
                <div class="identifybox" @click="refreshCode">
                  <sidentify :identifyCode="identifyCode"></sidentify>
                </div>
            </el-form-item>
            <!-- 登录按钮 -->
            <el-form-item>
              <el-button type="primary" @click="login('loginForm')" style="text-align: center;width: 100px">登  录</el-button>
            </el-form-item>
          </el-form>
      </el-row>
      <!-- 注册和忘记密码链接 -->
      <div class="link">
        <el-link type="primary" :underline="false" href="/register">注册新账号</el-link>
      </div>
    </div>
  </div>
</template>
<script>
  import {designOpera} from './api'
  import { Loading } from 'element-ui'
  import sidentify from './sidentify'
export default {
  
components: { sidentify },
  name: 'Login',
  data() {
    const validateVerifycode = (rule, value, callback) => {
      if (value === "") {
        callback(new Error('请输入验证码'))
      } else if (value !== this.identifyCode) {
        console.log('验证码:', value);
        callback(new Error('验证码不正确!'))
      } else {
        callback()
      }
    }
    return {
      // 表单数据

      loginForm: {
        username: '',  //用户名
        password: '',  //密码
        verifycode:''
      },
      identifyCodes: "1234567890", //验证码的数字库
      identifyCode: "",  // 验证码组件传
      
      rules: {
        //表单验证（用户名验证规则）
        username: [
          {required: true,message: '账号不能为空', trigger: 'blur'},
          { max: 20, message: '账号长度最长20位', trigger: 'blur' }
        ],
        //表单验证（密码验证规则）
        password: [
          {required: true, message: '密码不能为空', trigger: 'blur'},
          { min: 6, message: '密码长度最少为6位', trigger: 'blur' }
        ],
        verifycode:[
          { required: true, trigger: 'blur', validator: validateVerifycode }
        ]
      },
    }
  },
//页面初始化
  mounted() {
    this.logincheck();
  },
//方法定义
  methods: {
    //检查登录是否过期
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){
            this.$router.push({path:'/login'})
          }
          if(data.data!=null){
            console.log(data)
            sessionStorage.setItem('username',data.data.user) //将后端传的username存入session
            this.$router.push({path:'/home'})
          }
        })
      },
    //登录方法
    login(formName) {
      // 表单验证通过，可进行操作
      this.$refs[formName].validate((valid) => {
        if (valid) {
          designOpera({
            opera_type:'login',  //操作类型
            username:this.loginForm.username,  //用户名
            password:this.$md5(this.loginForm.password),  //密码md5加密
          })
            .then(data=>{
              console.log(data);
              if (data.code==0) {  //登录成功，并提示
                this.$notify({
                  type: 'success',
                  message: '欢迎你,' + this.loginForm.username + '!',
                  duration: 3000
                });
                this.$router.push({path:'/home'});  //跳转到用户主页面
                sessionStorage.setItem("username",this.loginForm.username)   //将用户名存入session中
                this.$emit("state");  //将状态传到base页面
              }
              else {
                if(data.code==-5){  //未注册,提示未注册
                    this.$message({
                    type: 'error',
                    message: '您还未注册账户，请注册',
                    showClose: true
                  });
                }
                else { //账号或密码错误提示
                    this.$message({
                    type: 'error',
                    message: '账号或密码错误',
                    showClose: true
                  });
                }
              }
            })
        } else {
          return false;  //表单验证错误返回false
        }
      })
    },
    //验证码----start
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    },
    refreshCode() {
      this.identifyCode = "";
      this.makeCode(this.identifyCodes, 4);
    },
    makeCode(o, l) {
      for (let i = 0; i < l; i++) {
        this.identifyCode += this.identifyCodes[
          this.randomNum(0, this.identifyCodes.length)
        ];
      }
      // console.log("this.identifyCode:", this.identifyCode);
    },
    created() {
    this.refreshCode(); //初始化验证码
  },
  mounted() {
    // 验证码初始化
    this.identifyCode = '';
    this.makeCode(this.identifyCodes, 4);
 
  },
  }
}
</script>

<style scoped>
  /* 主页面样式 */
  .login {
    position: absolute;  /*绝对定位*/
    width:100%;
    height:100%;
    background-color: #E4E7ED;
  }
/* 标题样式 */
  .title {
    font-size: large;  /*字体大小*/
    font-weight: bolder;  /*字体加粗*/
    text-align: center;
    color:black;
  }
/* 登录部分div样式 */
  .main_login {
    position: absolute;
    left:48%;
    top:40%;
    width:320px;
    height:350px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px;  /*圆角边框*/
    background: #F2F6FC;
  }
  /* 表单样式 */
  .el-form {
    padding-top: 5%;
    padding-left: 10%;
    padding-right: 10%;
    width:280px;
  }
  /* .el-row标签样式 */
  .el-row {
    height: 100%;
    width: 100%;
  }
  /* 文字链接div样式 */
  .link{
    margin-top: -13%;
    text-align: center;   /* 文本居中 */
    margin-left: -5%;
  }
  /* 文字链接样式 */
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }
</style>
