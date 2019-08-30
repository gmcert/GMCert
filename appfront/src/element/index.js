// 导入自己需要的组件
import { Select, Option, OptionGroup, input, Divider, Button, Form, Link, formItem,radio, upload, checkbox, loading, dialog } from 'element-ui';
// import { radio-button,radio-group  } from 'element-ui';

import radioBtn from 'element-ui/packages/radio-button';
import radioGrp from 'element-ui/packages/radio-group';

const element = {
  install: function (Vue) {
    Vue.use(Select);
    Vue.use(Option);
    Vue.use(OptionGroup);
    Vue.use(Button);
    Vue.use(Form);
    Vue.use(dialog);
    Vue.use(Link);
    Vue.use(input);
    Vue.use(formItem);
    Vue.use(radio);
    Vue.use(radioBtn);
    Vue.use(radioGrp);
    Vue.use(upload);
    Vue.use(checkbox);
    Vue.use(loading);
    Vue.use(Divider);
  }
}
export default element
