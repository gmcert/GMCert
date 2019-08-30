<template>
    <div>
    	<div class="title_box">
    		<a href="#" @click="backPage" type="primary">
    			<img src="../assets/gmcertlogo.png" class="img_size">
    		</a>
		  </div>

			<h1>线上签发证书</h1>
			<div class="formClass">
				<el-form ref="formTable" style="width: 500px;margin: 0 auto;" :model="formTable" label-width="120px" align="left">
				  <el-form-item label="设置证书算法：">
				  	<el-radio-group v-model="formTable.algorithm" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="国密SM2算法"></el-radio-button>
				      <el-radio-button label="RSA算法"></el-radio-button>
				      <el-radio-button label="ECC算法"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>

				  <el-form-item v-if="formTable.algorithm=='国密SM2算法'" label="国密证书类型：">
				  	<el-radio-group v-model="formTable.digestflag" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="">签名证书</el-radio-button>
				      <el-radio-button label="加密证书"></el-radio-button>
				      <el-radio-button label="全能证书"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>

				  <el-form-item v-if="formTable.algorithm=='RSA算法'" label="选择密钥长度：">
				  	<el-radio-group v-model="formTable.keylength" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="1024"></el-radio-button>
				      <el-radio-button label="2048"></el-radio-button>
				      <el-radio-button label="4096"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>

				  <el-form-item v-if="formTable.algorithm=='ECC算法'" label="选择椭圆曲线：">
				  	<el-radio-group v-model="formTable.ellipticCurve" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="prime256v1"></el-radio-button>
				      <el-radio-button label="brainpoolP256r1"></el-radio-button>
				      <el-radio-button label="frp256r1"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>

				  <el-form-item label="国家/C：">
				    <el-input v-model="formTable.countryCode" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="省份/S：">
				    <el-input v-model="formTable.province" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="城市/L：">
				    <el-input v-model="formTable.city" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="组织/O：">
				    <el-input v-model="formTable.organization" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="部门/OU：">
				    <el-input v-model="formTable.organizationalUnit" class="inputLen"></el-input>
				  </el-form-item>
				  <!-- <el-form-item label="邮箱：">
				    <el-input v-model="formTable.email" class="inputLen"></el-input>
				  </el-form-item> -->
				  <el-form-item label="主题名称/CN：">
				    <el-input v-model="formTable.commonName" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="证书链选项：">
              <el-checkbox v-model="checked" label="自动包含CA证书链" border size="medium"></el-checkbox>
				  </el-form-item>
				  <el-form-item label="输出格式：">
				  	<el-radio-group v-model="formTable.outflag" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="密钥+证书" fill="#9999FF"></el-radio-button>
				      <el-radio-button label="PKCS12/PFX" fill="#9999FF"></el-radio-button>
				      <el-radio-button label="JKS" fill="#9999FF"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>
				  <el-form-item v-if="" label="保护密码：">
				  	<el-input type="password" v-model="formTable.propassword" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="序列号：">
				  	<el-input type="text" v-model="formTable.serialNumber" class="inputLen"></el-input>
				  </el-form-item>

				  <el-divider></el-divider>
				  <el-form-item>
				    <el-button type="primary" round @click="onSubmit(formTable)">签发证书</el-button>
				  </el-form-item>
				</el-form>
			</div>

    </div>
</template>

<script>
    // import headTop from '@/components/headTop'
    // import {cityGuess, addShop, searchplace, foodCategory} from '@/api/getData'
    // import {baseUrl, baseImgPath} from '@/config/env'
    import Bus from '@/api/bus.js'
    import https from '@/http.js'
    import {mapActions, mapState,mapGetters} from 'vuex'
    export default {
    	data(){
    		return {
    			activeName: 'first',
    			formTable:{
    				algorithm:"",
    				ellipticCurve:"",
    				name:"",
	    			CAvalue:"",
	    			keyvalue:"",
	    			digestvalue:"",
	    			startDate:"",
	    			desc:"",
	    			serialNumber:"",
	    			countryCode:"",
	    			province:"",
	    			city:"",
	    			organization:"",
	    			organizationalUnit:"",
	    			email:"",
	    			commonName:"",
	    			propassword:"",
	    			outflag:"仅证书",
	    			digestflag:""
    			},
    			checked:true,
    			CAoptions:[],
    			keyoptions:[],
    			digestoptions:[],
    			certtype:"",
    			certnum:3
    		}
    	},

	    created(){
    		this.initData();
    	},
    	computed:{
		     certData(){
		       return this.$store.getters.certInfo;
		     },
		     signType(){
		       return this.$store.getters.signType;
		     }
		},
    	methods: {
    		async initData(){
    			let res = this.certData;
    			this.formTable.name = res.commonName;
    			this.formTable.city = res.city;
    			this.formTable.commonName = res.commonName;
    			this.formTable.countryCode = res.countryCode;
    			this.formTable.organization = res.organization;
    			this.formTable.organizationalUnit = res.organizationalUnit;
    			this.formTable.province = res.province;
    			if (this.certData.num == 0) {
    				this.certtype = "RSA算法证书";
    			}else if(this.certData.num == 1){
    				this.certtype = "国密算法证书";
    			}else if(this.certData.num == 2){
    				this.certtype = "ECC算法证书";
    			}
    			this.certnum = this.certData.num;
    		},
    		async onSubmit(form){
    			try{
    				form.csrfile = this.certData.csrfile;
    				// if (form.digestflag=="签名证书") {
    				// 	form.digestflag=false;
    				// }else{
    				// 	form.digestflag=true;
    				// }
    				form.num = this.certnum;
    				console.log(form.num);
    				https.fetchPost('/utils/sigin_cert',form).then((data) => {
    					let result = data.data;
    					if (result.flag=="Success") {
    						let fileNm = result.file;
    						this.$store.commit('saveCertInfo',{});
    						this.$store.commit('saveCertUrl',fileNm);
    						this.$router.push({name:"downCert"})
    						// this.formTable.digestflag="签名证书";
    						// window.open("/utils/download?0="+fileNm);
    					}
	                }).catch((err) => {
	                        console.log(err)
	                    }
	                )
    			}catch(e){
    				console.log(e);
    			}
    		},
    		backPage(){
    			this.$router.push({name:"mainPage"});
    		}
		}
    }
</script>

<style lang="less" scoped>
	.title_box{
		width: 100%;
		height: 100px;
		line-height: 100px;
		vertical-align: middle;
		clear: both;
		text-align: left;
		display: inline-block;
	}
	.img_size{
		float: left;
		vertical-align: middle;
		width: 262px;
		height: 52px;
	}
	.formClass{
		height: 300px;
		/*min-height: 1000px;*/
		margin: 0 auto;
		border: 1px solid #DCDFE6;
		border-radius: 2px;
		padding: 50px;
		width:40%;  
	    padding-bottom: 30%;  
	}
	/*.inputLen{
		width: 350px;
	}*/
</style>
