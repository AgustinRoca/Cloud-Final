<template>
  <div>
    <h1>Locate face from picture</h1>
    <GenerateFromImageForm @generated="facesGenerated"/>
    <FacesModal :showModal="showModal" :imgs_bytes="[img_bytes]" :zs="[z]" @close="closeModal"/>
  </div>
</template>
<script>
import { defineComponent } from 'vue';
import GenerateFromImageForm from '../components/GenerateFromImageForm.vue'
import FacesModal from '../components/FacesModal.vue'

// Components

export default defineComponent({
  name: 'GenerateFromImageView',
  components: {
    GenerateFromImageForm,
    FacesModal,
  },
  data() {
    return {
      showModal: false,
      z: null,
      img_bytes: null
    }
  },
  methods: {
    closeModal(){
      this.showModal = false
    },
    facesGenerated(img_bytes, z){
      this.showModal = true
      this.img_bytes = img_bytes
      this.z = z
    }
  }
});
</script>
