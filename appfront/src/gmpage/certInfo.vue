<template>
    <div>
    	<div class="title_box">
			<img src="../assets/gmcertlogo.png" class="img_size">
		</div>
		<div style="padding: 50px;">

	    	<el-form ref="formTable" style="width: 400px;margin: 0 auto;" :model="formTable" label-width="120px">
			  
				
			  <el-form-item label="国家编码：">
			    <el-input v-model="formTable.countryCode" class="inputLen"></el-input>
			  </el-form-item>
			  <el-form-item label="省份：">
			    <el-input v-model="formTable.province" class="inputLen"></el-input>
			  </el-form-item>
			  <el-form-item label="城市：">
			    <el-input v-model="formTable.city" class="inputLen"></el-input>
			  </el-form-item>
			  <el-form-item label="公司：">
			    <el-input v-model="formTable.organization" class="inputLen"></el-input>
			  </el-form-item>
			  <el-form-item label="部门：">
			    <el-input v-model="formTable.organizationalUnit" class="inputLen"></el-input>
			  </el-form-item>
			  <el-form-item label="通用名称：">
			    <el-input v-model="formTable.commonName" class="inputLen"></el-input>
			  </el-form-item>

			  <el-form-item label="国密证书类型：">
			  	<el-radio-group v-model="formTable.digestflag">
			      <el-radio-button label="签名证书"></el-radio-button>
			      <el-radio-button label="加密证书"></el-radio-button>
			    </el-radio-group>
			  </el-form-item>
			  <el-form-item>
			    <el-button type="primary" @click="onSubmit(formTable)">立即创建</el-button>
			    <el-button  @click="backPage">返回上一页</el-button>
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
	    			digestflag:"签名证书"
    			},
    			CAoptions:[],
    			keyoptions:[],
    			digestoptions:[],

    		}
    	},

	    created(){
    		this.initData();
    	},
    	computed:{
		     certData(){
		       return this.$store.getters.certInfo;
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
    		},
    		async onSubmit(form){
    			try{
    				form.csrfile = this.certData.csrfile;
    				if (form.digestflag=="签名证书") {
    					form.digestflag=false;
    				}else{
    					form.digestflag=true;
    				}
    				https.fetchPost('/utils/sigin_cert',form).then((data) => {
    					let result = data.data;
    					if (result.flag=="Success") {
    						let fileNm = result.file;
    						this.$store.commit('saveCertInfo',{});
    						this.formTable.digestflag="签名证书";
    						window.open("/utils/download?0="+fileNm);
    			// 			https.fetchGet('/utils/download',result.file).then((resdata) => {
    			// 				// window.open("/utils/download?0="+this.formTable);
    			// 				let blob = new Blob([resdata.data], {type: "application/x-tar"});
							// 　　let objectUrl = URL.createObjectURL(blob);
							// 　　window.location.href = objectUrl;
    			// 			}).catch((err) => {
		     //                    console.log(err)
		     //                });
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
	.logoclass{
		width: 600px;
		height: 400px;
		margin: 250px auto;
		text-align: center;
	}
	.title_box{
		width: 100%;
		height: 100px;
		line-height: 100px;
		vertical-align: middle;
		clear: both;
		display: inline-block;
	}
	.img_size{
		float: left;
		vertical-align: middle;
		width: 262px;
		height: 52px;
	}
	/*.inputLen{
		width: 350px;
	}*/
</style>
