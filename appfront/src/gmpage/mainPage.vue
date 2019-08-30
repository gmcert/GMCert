<template>
    <div>
    	<div class="title_box">
			<a href="#" @click="backPage" type="primary">
    			<img src="../assets/gmcertlogo.png" class="img_size">
    		</a>
			<span class="btn_inline">
				<el-button type="primary" @click="">登录</el-button>
				<el-button @click="">注册</el-button>
			</span>
		</div>
		<div class="main_btngroup">
			<img src="../assets/gmtitlelogo.jpg" class="img_titsize">
			<div class="btn_group">
				<div class="btn_img">
					<a href="#" @click="dialogVisible=true">
						<img src="../assets/btncsr.png" alt="">
					</a>
					<a href="#" @click="hrefsub">
						<img src="../assets/btnnew.png" alt="">
					</a>
					<a href="#">
						<img src="../assets/btncheck.png" alt="">
					</a>
				</div>
				<div class="btn_grouptxt">
					<a href="#" @click="dialogVisible=true">上传证书请求</a>
					<a href="#" @click="hrefsub">网站直接生成</a>
					<a href="#">查看证书信息</a>
				</div>
				<div class="btn_boxtxt">
					<div style="opacity: 0.5">线下自行生成私钥，上传csr/req/pkcs10等格式证书请求文件</div>
					<div style="opacity: 0.5">线上生成私钥，同时申请签发证书，合并下载。</div>
					<div style="opacity: 0.5">上传已有证书，查看证书信息，校验证书链信任关系等</div>
				</div>
			</div>
			
		</div>
		<div class="footer">
				<div class="footer_div">
					<a href="#">关于GMCERT</a>
					<a href="#">联系我们</a>
					<a href="#">意见反馈</a>
				</div>
				<div style="opacity: 0.5;color: #000;">
					Copyright(C)2019 GMCert
				</div>
			</div>
<el-dialog
  title="上传CSR文件"
  :visible.sync="dialogVisible"
  width="30%"
  top="38vh">
  			<el-upload
			  class="upload-demo"
			  drag
			  accept=".csr,.req,.pem,.txt"
			  action="/utils/upload"
			  multiple
      		  :on-success="handleSuccess">
			  <i class="el-icon-upload"></i>
			  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
			  <div class="el-upload__tip" slot="tip">只能上传csr文件</div>
			</el-upload>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
</el-dialog>
    </div>

</template>

<script>
	// admin Ybxgwolingstaff
    import Bus from '@/api/bus.js'
    import {mapActions, mapState} from 'vuex'
    export default {
    	data(){
    		return {
    			options: [{
		          value: '选项1',
		          label: '国密签名'
		        }, {
		          value: '选项2',
		          label: '国密加密'
		        }, {
		          value: '选项3',
		          label: '签名+加密证书'
		        }, {
		          value: '选项4',
		          label: 'RSA证书'
		        }, {
		          value: '选项5',
		          label: 'ECC'
		        }],
		        value: '',
		        logo: 'this.src="' + require('../assets/gmcertlogo.png') + '"',
		        dialogVisible:false
    		}
    	},
    	mounted(){
    		this.initData();
    	},
    	methods: {
    		async initData(){
    			
    		},
    		handleSuccess(response, file, fileList){
    			try{
	    			if (response.flag=="Success") {
	    				let obj = {};
	    				obj.city = response.data.city;
	    				obj.commonName = response.data.commonName;
	    				obj.countryCode = response.data.countryCode;
	    				obj.organization = response.data.organization;
	    				obj.organizationalUnit = response.data.organizationalUnit;
	    				obj.province = response.data.province;
	    				obj.csrfile = response.csrfile;
	    				obj.num = response.num;
	    				this.$store.commit('saveCertInfo',obj);
	    				this.$router.push({name:"submitForm"})
	    			}
    			}catch(e){
    				console.log(e);
    			}
    		},
    		hrefsub(){
    			this.$router.push({name:"subForm"});
    		},
    		backPage(){
    			this.$router.push({name:"mainPage"});
    		}
		}
    }
</script>

<style lang="less" scoped>

	.main_btngroup{
		width: 600px;
		margin: 10px auto;
		/*text-align: center;*/
	}
	.title_box{
		width: 100%;
		height: 100px;
		/*line-height: 100px;
		vertical-align: middle;*/
		clear: both;
		display: inline-block;
	}
	.btn_inline{
		float: right;
		vertical-align: middle;
		display: inline-block;
	}
	.img_size{
		float: left;
		vertical-align: middle;
		width: 262px;
		height: 52px;
	}
	.img_titsize{
		width: 600px;
		height: 214px;
		margin: 0 auto;
	}
	.btn_group .btn_img{
		clear: both;
		padding: 35px;
	}
	.btn_group .btn_img img{
		width: 113px;
		height: 113px;
		margin: 0 30px;
		float: left;
	}
	.btn_grouptxt{
		padding: 30px;
	}
	.btn_grouptxt a{
		margin: 15px 28px;
		float: left;
		font-size: 20px;
		text-decoration: none;
		color: #000;
	}
	.btn_grouptxt a:visited {
     color: #000;
     text-decoration: none;
    }
    .btn_grouptxt a:hover {
     color: #E6A23C;
     text-decoration: underline;
    }
	.btn_boxtxt{
		clear: both;
		width: 600px;
		padding: 0 35px;
	}
	.btn_boxtxt div{
		width: 113px;
		height: 113px;
		float: left;
		display: inline;
		margin: 0 30px;
		vertical-align: middle;
		border-radius: 14px;
		font-size: 14px;
	}
	.footer{
		width: 100%;
		height: 50px;
		margin: 0 auto;
		display: block;
		margin: 0 auto;
		position: absolute;
		z-index: 0;
		bottom: 0;	
	}
	.footer_div{
		margin: 0 auto;
		opacity: 0.5;
	}
	.footer_div a{
		margin: 0 10px;
		color: #000;
     	text-decoration: none;
	}
	.footer_div a:visited {
     color: #000;
     text-decoration: none;
    }
    .footer_div a:hover {
     color: #E6A23C;
     text-decoration: underline;
    }
    .el-upload-dragger{
    	width: 100%;
    	height: 100%;
    }
</style>
