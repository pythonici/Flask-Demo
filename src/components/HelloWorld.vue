<template>
<b-modal ref="editResModal"
         id="res-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-sn-edit-group"
                label="Title："
                label-for="form-sn-edit-input">
      <b-form-input id="form-sn-edit-input"
                    type="text"
                    v-model="editForm.title"
                    required
                    >
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-teacher-edit-group"
                  label="Author："
                  label-for="form-teacher-edit-input">
        <b-form-input id="form-teacher-edit-input"
                      type="text"
                      v-model="editForm.author"
                      required
                      >
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-learnt-edit-group">
      <b-form-checkbox-group v-model="editForm.learn" id="form-checks">
       <b-form-checkbox value="true">Read?</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-form>
</b-modal>
<b-modal ref="addResModal"
         id="res-modal"
         title="Add a new book"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-title-group"
                label="Title："
                label-for="form-title-input">
      <b-form-input id="form-title-input"
                    type="text"
                    v-model="addResForm.title"
                    required
                    placeholder="Enter title">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-group"
                  label="Author："
                  label-for="form-author-input">
        <b-form-input id="form-author-input"
                      type="text"
                      v-model="addResForm.author"
                      required
                      placeholder="Enter author">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-learn-group">
      <b-form-checkbox-group v-model="addResForm.learn" id="form-checks">
        <b-form-checkbox value="true">Read?</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1 align="left">Books</h1>
        <hr><br><br>
        <alert :message="message" :variant="alertvariant" v-if="ShowMessage"></alert>
        <br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.res-modal>Add Book</button>
        <br><hr>
        <table class="table table-hover ">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
    
            <tr v-for="(books,index) in books" :key="index">
              <td>{{books.title}}</td>
              <td>{{books.author}}</td>
              <td>
              <span v-if="books.learn">是</span>
              <span v-else>否</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.res-update-modal @click="editRes(books)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteRes(books)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>e
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import FlashMessage from './FlashMessage.vue';
export default {
  name: 'HelloWorld',
  data(){
    return {
      books:[],
       addResForm: {
          title: '',//标题
          author: '',//作者
          learn: [],//是否学习
      },
      editForm: {
          title: '',
          author: '',
          learn: [],
      },
      message:'',
      alertvariant:'',
      showMessage:false,
    };
  },
   components: {
    alert: FlashMessage,
  },
  methods:{
  
    getMessage(){
      const path = "http://localhost:5000/all_books"; //服务端地址
      axios.get(path)  //跨域请求
      .then((res)=>{
        this.books = res.data.books;
        })
      .catch((error)=>{
        console.error(error);
      });
    },
      editRes(r) {
  this.editForm = r;
},
removeRes(title) {
    const path = `http://localhost:5000/update_info/${title}`;
    axios.delete(path)
        .then((res) => {
        this.message = res.data.message;
        var success = res.data.status;
        if (success == 'failed') {
            this.alertvariant = 'danger';
        } else if (success == 'success') {
            this.alertvariant = 'success';
        } else {
            this.alertvariant = 'info';
        }
        this.showMessage = true;
        this.getMessage();
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getMessage();
        });
},
onDeleteRes(r) {
    this.removeRes(r.title);
},
   addRes(payload) {
      const path = 'http://localhost:5000/all_books';
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          var success = res.data.status;
          if (success == 'failed') {
              this.alertvariant = 'danger';
          } else if (success == 'success') {
              this.alertvariant = 'success';
          } else {
              this.alertvariant = 'info';
          }
          this.getMessage();
          this.ShowMessage=true;
        })
        .catch((error) => {
          console.log(error);
          this.getMessage();
        });
    },
    //清空表单
    initForm() {
      this.addResForm.title = '';
      this.addResForm.author = '';
      this.addResForm.learn = [];
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.learn = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      console.log(this.$refs.addResModal);
      this.$nextTick(() => {this.$refs.addResModal.hide();});
      
     
      let learn = false;
      if (this.addResForm.learn[0]) learn = true;
      const payload = {
        title: this.addResForm.title,
        author: this.addResForm.author,
        learn,
      };
      this.addRes(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addResModal.hide();
      this.initForm();
    },
    onSubmitUpdate(evt) {
    evt.preventDefault();
    //this.$refs.editResModal.hide();
    let learn = false;
    if (this.editForm.learn[0]) learn = true;
    const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        learn,
    };
    this.updateRes(payload, this.editForm.title);
},
updateRes(payload, title) {
    const path = `http://localhost:5000/update_info/${title}`;
    axios.put(path, payload)
        .then((res) => {
        this.message = res.data.message;
        this.alertvariant = 'success';
        this.showMessage = true;
        this.getMessage();
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getMessage();
        });
},
onResetUpdate(evt) {
    evt.preventDefault();
    this.$refs.editResModal.hide();
    this.initForm();
    this.getMessage();
},
    },
  created(){
    this.getMessage();
  },
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
