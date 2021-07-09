<template>
  <div class="todo-list pt-2">
    <h3 class="py-3">
      Todo List
    </h3>
    <!-- Start Create New Taks stuff -->
    <div v-if="is_loading_tasks == false" @click="is_creating_task = true;" class="btn btn-outline-primary float-end mx-5 mb-2">Create New Task</div>
    <div v-if="is_loading_tasks == true" >loading...<i  class="fas fa-spinner fa-pulse"></i></div>

    <div v-if="is_saving_tasks == true" >saving...<i  class="fas fa-spinner fa-pulse"></i></div>
    <div v-if="is_creating_task == true" class="add-todo-module">
      <div @click="is_creating_task = false;newTask.desc = null;" class="add-todo-exit"><i class="exit-icon far fa-times-circle"></i></div>
      <h4 class="text-white font-weight-bold mt-3">Enter TODO Task</h4>
      <textarea v-model="newTask.desc" class="add-todo-text"></textarea>
      <div @click="createNewTODOItem" class="add-todo-submit-btn btn btn-primary">Create Task</div>
    </div>
    <!-- End Create New Taks stuff -->
    <!-- Edit Task Stuff -->
    <div v-if="is_editing_task == true" class="add-todo-module">
      <div @click="is_editing_task = false;edit_task_text = null;edit_target = null;" class="add-todo-exit"><i class="exit-icon far fa-times-circle"></i></div>
      <h4 class="text-white font-weight-bold mt-3">Enter TODO Task</h4>
      <textarea v-model="edit_task_text" class="add-todo-text"></textarea>
      <div @click="finishEditTask" class="add-todo-submit-btn btn btn-primary">Create Task</div>
    </div>
    <!-- Start Table for displaying todo items -->
    <table id="todo-list-table" ref="todo" class="table table-striped" style="width:100%">
        <thead>
          <tr>
            <th class="h4">Items</th>
            <th class="h4">Times</th>
            <th class="h4">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in todoListItems" :key="item">
            <th class="todo-item px-5">{{item.desc}}</th>
            <th>{{item.time}}</th>
            <th class="action-item">
              <div @click="startEditTask(index)" class="btn btn-outline-success mx-2">Edit</div>
              <div @click="deleteTodoItem(index)" class="btn btn-outline-danger mx-2">Delete</div>
            </th>
          </tr>
        </tbody>
    </table>
    <!-- End Table for displaying todo items -->
    <div v-if="todoListItems.length == 0">There are NO tasks.</div>
    <div class="btm-padding"></div>
  </div>
</template>

<script>
// import firebase from '../utilities/firebase'
import axios from 'axios'

export default {
  props: ['authUser'],
  data () {
    return {
      is_creating_task: false,
      is_editing_task: false,
      edit_task_text: null,
      edit_target: null,
      newTask: {
        desc: null,
        time: null
      },
      todoListItems: [
      ],
      is_saving_tasks: false,
      is_loading_tasks: false,
    }
  },
  mounted(){
    // this.$nextTick(funciton () {
    //   console.log(this.$refs.myid)
    // });
    // document.getElementById('todo-list-table').DataTable();
    this.loadTasksData()
  },
  methods: {
  //   // Create new TODO List task and add it to other tasks
    createNewTODOItem(){
      console.log("Create Todo Item");
      // console.log(this.newTask.desc);

      const curTime = new Date()
      const date = curTime.getFullYear()+'-'+(curTime.getMonth()+1)+'-'+curTime.getDate()
      const time = curTime.getHours() + ":" + curTime.getMinutes() + ":" + curTime.getSeconds();
      const convTime = this.convertTime(time);
      console.log(convTime)
      this.newTask.time = date + ' ' + convTime;
      const newItem = { ...this.newTask};
      // this.todoListItems.unshift(newItem);

      // this.saveTaskData();
      this.insertTodoList(newItem);
      this.newTask.desc = null;
      this.newTask.time = null;
      this.is_creating_task = false;
    },
    // Insert new task into database
    insertTodoList(item) {
      axios.post("/api/todo_list/insert", item).then(
        (response) => {
          this.todoListItems.unshift(response.data.entry_list[0]);
        },
        (error) => {
          console.log(error);
        }
      );
    },
  //   // Edit Task Functions
    startEditTask(index){
      this.edit_target = index;
      this.edit_task_text = this.todoListItems[index].desc;
      this.is_editing_task = true;
    },
    finishEditTask(){
      this.todoListItems[this.edit_target].desc = this.edit_task_text;
      // this.saveTaskData();
      this.edit_target = null;
      this.edit_task_text = null;
      this.is_editing_task = false;
    },
    // End Edit Task Functions
    // Delte Todo List item
    deleteTodoItem(index){
      console.log(index);
      const id_obj = {'id': this.todoListItems[index].id}
      axios.post("/api/todo_list/delete", id_obj).then(
        (response) => {
          console.log(response.data);
          this.todoListItems.splice(index, 1);
        },
        (error) => {
          console.log(error);
        }
      );
      // this.saveTaskData();
    },
    // Laod all the todo_list data
    loadTasksData(){
      axios.get("/api/todo_list/load").then(
        (response) => {
          this.todoListItems = response.data.entry_list;
        },
        (error) => {
          console.log(error);
        }
      );
    },
  //   // Start Firebase save and load functions
  //   saveTaskData(){
  //     this.is_saving_tasks = true;
  //     const processed_task_data = {'tasks': this.todoListItems}
  //     console.log(processed_task_data);
  //     // convert your object into a JSON-string
  //     var jsonString = JSON.stringify(processed_task_data);
  //     // create a Blob from the JSON-string
  //     var new_blob = new Blob([jsonString], {type: "application/json"})
  //     firebase.storage().ref('users/' + this.authUser.uid + '/savedTask.json').put(new_blob).then(() => {
  //       this.is_saving_tasks = false;
  //       // this.resetAddCardDisplay()
  //       console.log('Save Worked');
  //     }).catch(error => {
  //       console.log('Save failed' + error);
  //       this.is_saving_tasks = false;
  //       // this.resetAddCardDisplay()
  //     })
  //   },
  //   loadTasksData()
  //   {
  //     this.is_loading_tasks = true;
  //     firebase.storage().ref('users/' + this.authUser.uid + '/savedTask.json').getDownloadURL().then((savedDataURL) => {
  //       axios.get(savedDataURL)
  //       .then((response) => {
  //         console.log(response.data)
  //         if(response.data.tasks != undefined)
  //         {
  //           this.todoListItems = response.data.tasks;
  //         }
  //         else 
  //         {
  //           this.todoListItems = {};
  //         }
  //         this.is_loading_tasks = false;
  //         // this.is_card_data_loaded = true;
  //         // this.checkForCardDisplay();
  //       });
  //       console.log('Profile Tasks Load Worked');
  //     }).catch(error => {
  //       // this.is_card_data_loaded = true;
  //       console.log('Load failed' + error);
  //       this.is_loading_tasks = false;
  //     })
  //   },
  //   // End Firebase save and load functions
  //   // Convert military time to standard time.
    convertTime(input){
      var time = input; // your input

      time = time.split(':'); // convert to array

      // fetch
      var hours = Number(time[0]);
      var minutes = Number(time[1]);
      var seconds = Number(time[2]);

      // calculate
      var timeValue;

      if (hours > 0 && hours <= 12) {
        timeValue= "" + hours;
      } else if (hours > 12) {
        timeValue= "" + (hours - 12);
      } else if (hours == 0) {
        timeValue= "12";
      }
      
      timeValue += (minutes < 10) ? ":0" + minutes : ":" + minutes;  // get minutes
      timeValue += (seconds < 10) ? ":0" + seconds : ":" + seconds;  // get seconds
      timeValue += (hours >= 12) ? " P.M." : " A.M.";  // get AM/PM

      // show
      // console.log(timeValue);
      return timeValue;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.add-todo-module{
  background: rgb(93, 178, 211);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50%;
  height: 50%;
  border-radius: 12px;
}

.add-todo-text {
  position: absolute;
  top: 15%;
  left: 0;
  width: 100%;
  height: 60%;
  text-align: center;
  padding: 22px;
}

.add-todo-submit-btn {
  position: absolute;
  bottom: 0;
  margin-bottom: 2%;
  transform: translate(-50%, 0);
  font-size: 16px;
}

.add-todo-exit{
  position: absolute;
  top: 0;
  right: 0;
  width: 5%;
  height: 5%;
  margin: 12px 12px;
  color: rgb(255, 121, 121)!important;
}

.exit-icon{
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
}

.exit-icon:hover{
  color: rgb(255, 0, 0)!important;
  cursor: pointer;
}
.todo-item{
  width: 55%;
  text-align: left;
}

.btm-padding {
  height: 100px;
}
</style>
