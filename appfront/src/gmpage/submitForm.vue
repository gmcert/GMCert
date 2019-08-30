<template>
    <div>
    	<div class="title_box">
    		<a href="#" @click="backPage" type="primary">
    			<img src="../assets/gmcertlogo.png" class="img_size">
    		</a>
			
		</div>
			<div class="formClass">
				<span v-if="certtype">{{certtype}}<a href="#">查看证书</a></span>
				<h1>为CSR签发证书</h1>
				<el-form ref="formTable" style="width: 500px;margin: 0 auto;" :model="formTable" label-width="120px"  align="left">

				  <el-form-item label="国密证书类型：">
				  	<el-radio-group v-model="formTable.digestflag" size="medium" fill="#CCE" text-color="#000">
				      <el-radio-button label="签名证书"></el-radio-button>
				      <el-radio-button label="加密证书"></el-radio-button>
				      <el-radio-button v-show="certData.num==1" label="全能证书"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>
				  
				 <!--  <el-form-item label="签发CA：">
				    <el-select class="inputLen" v-model="formTable.CAvalue" placeholder="请选择签发CA">
					    <el-option
					      v-for="item in CAoptions"
					      :key="item.value"
					      :label="item.label"
					      :value="item.value">
					    </el-option>
				    </el-select>
				  </el-form-item>

				  <el-form-item label="密钥位数：">
				    <el-select class="inputLen" v-model="formTable.keyvalue" placeholder="请选择密钥位数">
					    <el-option
					      v-for="item in keyoptions"
					      :key="item.value"
					      :label="item.label"
					      :value="item.value">
					    </el-option>
				    </el-select>
				  </el-form-item>

				  <el-form-item label="加密算法：">
				    <el-select class="inputLen" v-model="formTable.digestvalue" placeholder="请选择加密算法">
					    <el-option
					      v-for="item in digestoptions"
					      :key="item.value"
					      :label="item.label"
					      :value="item.value">
					    </el-option>
				    </el-select>
				  </el-form-item>

				<el-form-item label="起始日期：">
				    <el-date-picker
				    class="inputLen"
				      v-model="formTable.startDate"
				      type="date"
				      placeholder="选择日期"
				      format="yyyy 年 MM 月 dd 日">
				    </el-date-picker>
				  </el-form-item> -->
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
				      <el-radio-button label="仅证书" fill="#9999FF"></el-radio-button>
				    </el-radio-group>
				  </el-form-item>
				  <!-- <el-form-item label="扩展项：">
				  	<el-input type="textarea" v-model="formTable.desc" class="inputLen"></el-input>
				  </el-form-item>
				  <el-form-item label="序列号：">
				  	<el-input type="text" v-model="formTable.serialNumber" class="inputLen"></el-input>
				  </el-form-item> -->
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
	    			
	    			outflag:"仅证书",
	    			digestflag:"签名证书"
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
    				form.isNewKey = 0;

    				form.csrfile = this.certData.csrfile;
    				if (form.digestflag=="签名证书") {
    					form.digestflag=false;
    					form.gmType = 0;
    				}else if (form.digestflag=="加密证书") {
    					form.digestflag=true;
    					form.gmType = 1;
    				}else if (form.digestflag=="全能证书") {
						form.digestflag=true;
    					form.gmType = 2;
    				}
    				form.algType = this.certnum;
    				if (this.checked) {
    					form.isCombineChain = 1;
    				}else{
    					form.isCombineChain = 0;
    				}
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
