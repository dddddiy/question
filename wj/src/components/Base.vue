<!--
程序名：网站导航栏
功能：网站顶部导航栏
-->
<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo" @click="toIndex">
          <img src="/static/images/logo.png" class="logoImg">
          <span style="color: #303133">问了吗</span>
          <span style="font-size: 13px;margin-left: 5px;color: #606266">——免费的在线问卷系统</span>
        </div>
        <div style="float: right;margin-right: 50px;line-height: 60px;">
          <!-- 未登录时显示 -->
          <template v-if="!showname">
            <el-button type="primary" plain style="font-size: 15px;" @click="toLogin">登录</el-button>
            <el-button plain style="font-size: 15px;" @click="toRegiste">注册</el-button>
          </template>
          <!-- 登录时显示 -->
          <template v-else>
            <!-- 登录成功，显示用户名 -->
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                {{username}}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <!-- 退出登录 -->
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">问卷管理</el-dropdown-item>
                <el-dropdown-item command="c">修改密码</el-dropdown-item>
                <el-dropdown-item command="b">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </div>
      </el-header>
      <el-main style="padding: 0">
        <router-view @state="state"/>
      </el-main>
    </el-container>
    <el-dialog title="修改密码" :visible.sync="changepass" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item prop="old">
        <el-input @keyup.enter.native="chanpas('form')" icon="el-icon-search" placeholder="请输入旧密码" v-model="form.old">
                </el-input>
            </el-form-item>    
            <el-form-item prop="new">
        <el-input @keyup.enter.native="chanpas('form')" icon="el-icon-search" placeholder="请输入新密码" v-model="form.new">
                </el-input>
            </el-form-item>  
      </el-form>
        <el-button type="primary" @click="chanpas('form')" style="text-align: center;width: 100px">确定</el-button>
    </el-dialog>
  </div>
</template>
<script>
  import {designOpera} from './api'
  export default {
    name:'Base',
    data: function () {
      return {
        showname: false, //登录，注册按钮的显示状态
        username:'' ,//用户名
        changepass:false,
        newpass:'',
        form:{
          old:'',
          new:'',
        },
        rules:{
          old:[
            {required: true, message: '旧密码不能为空', trigger: 'blur'},
            { min: 6, message: '密码长度最少为6位', trigger: 'blur' }
          ],
          new:[
            {required: true, message: '新密码不能为空', trigger: 'blur'},
            { min: 6, message: '密码长度最少为6位', trigger: 'blur' }
          ]
        }
        
        
      }
    },
    methods:{
      toIndex(){
        this.$router.push({path:'/index'});
      },
      //检查登录是否过期
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){
            return false
          }
          else if(data.data!=null){
            console.log(data)
            sessionStorage.setItem('username',data.data.user) //将后端传的username存入session
          }
          this.state()  // 调用state方法
        })
      },
      // 跳转问卷管理页面方法
      toHome(){
        this.$router.push({path:'/home'})
      },
      // 跳转登录页面方法
      toLogin(){
        this.$router.push({path:'/login'})
      },
      // 跳转注册页面方法
      toRegiste(){
        this.$router.push({path:'/register'})
      },
      //判断session中是否存在数据，存在将showname置为true，否则false
      state(){
        console.log('state')
        console.log(sessionStorage.getItem('username'))
        if(sessionStorage.getItem('username')!=null){
          this.showname=true;
          this.username = sessionStorage.getItem('username')
        }
        else {
          this.showname = false
        }
      },
      //下拉菜单操作
      handleCommand(command){
        if(command=='a'){
          this.toHome();
        }
        else if(command=='c'){
          this.chan();
        }
        else if(command=='b'){
          this.exit();
        }
      },
      chan(){
        this.changepass=true;

      },
      chanpas(formName){
        this.$refs[formName].validate((valid) => {
          if(valid){
              designOpera({
            opera_type:'changepass',
            oldpass:this.$md5(this.form.old),
            newpass:this.$md5(this.form.new),
            cleannew:this.form.new
          
          })
          .then(data=>{
              console.log(data);
              if(data.code==0){
                this.$message({
                  type: 'success',
                  message: '修改成功!'
                });
                this.changepass=false  
              } 
              else{
                if(data.code==-4){
                    this.$message({
                    type: 'error',
                    message: '操作失败',
                    showClose: true
                  });
                }
                this.$message({
                  type: 'error',
                  message: '原密码错误',
                  showClose:true
                });
              }
            });
          }
          else{
            return false;
          }
        })
      },
      //登出
      exit(command){
        designOpera({
          opera_type:'exit',  // 操作类型
          username:sessionStorage.getItem('username')  //获取session中的用户名
        })
        .then(data=>{
          console.log(data);
          if(data.code==0){
            sessionStorage.clear()  //登出成功，清空session
            this.state()  // 调用state方法
            this.toLogin()  // 调用toLogin方法
          }
          else{
            this.$message({  // 报错友好提示
              type: 'error',
              message: '网络错误！',
              showClose: true
            });
          }
        })
      }
    },
    // 页面初始化
    mounted(){
      this.logincheck();
    },
  }
</script>
<style scoped>
  .main{
    position: absolute;
    width: 100%;
    height: 100%;
  }
  /* logo图片样式 */
  .logoImg{
    width: 30px;
    vertical-align: middle;
  }
  /* logo框样式 */
  .logo{
    height: 60px;
    display: inline-block;
    line-height: 60px;
    font-size: 20px;
    position: absolute;
    left: 100px;
    color: #303133;
    cursor: pointer;
  }
  .el-header{
    border-bottom: 2px solid #409EFF;
    background-color: white;
  }
   .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .demonstration {
    display: block;
    color: #8492a6;
    font-size: 14px;
    margin-bottom: 20px;
  }
</style>
