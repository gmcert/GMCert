
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
	certInfo: {},
	certUrl:"",
}

const mutations = {
	saveCertInfo(state, certInfo){
		state.certInfo = certInfo;
	},
	saveCertUrl(state, certUrl){
		state.certUrl = certUrl;
	}
}

const getters = {
    certInfo: state => {
        return state.certInfo
    },
    certUrl: state => {
        return state.certUrl
    }
}

const actions = {
	setCertInfo(context,data) {
		context.commit("saveCertInfo",data);
	}
}

export default new Vuex.Store({
	state,
	actions,
	mutations,
	getters
})
