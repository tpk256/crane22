<script>

import axios from "axios";
import { ref } from "vue";








export default  {

  data() {
    return {
      isModalOpen: ref(false), 
      tasks: [], 
      ws: null,

    };
  },

  methods:{

        drawTask(task){
          const taskId = task.id;
            if (task.state == 1){

              console.log(`Задание ${task.id} !!!!!!!!!!!`);
              
              const from_ = document.getElementById(`place-${task.from_id}`);
              const to = document.getElementById(`place-${task.to_id}`);

              const x0 = from_.getAttribute("x");
              const y0 = from_.getAttribute("y");

              const width0 = from_.getAttribute("width");
              const height0 = from_.getAttribute("height");

              const x1 = to.getAttribute("x");
              const y1 = to.getAttribute("y");

              const width1 = to.getAttribute("width");
              const height1 = to.getAttribute("height");


              const svg = document.querySelector("svg");
              if (!document.getElementById("arrow")) {
                  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
                  const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");

                  marker.id = "arrow";
                  marker.setAttribute("markerWidth", "10");
                  marker.setAttribute("markerHeight", "10");
                  marker.setAttribute("refX", "9");
                  marker.setAttribute("refY", "5");
                  marker.setAttribute("orient", "auto");
                  marker.setAttribute("markerUnits", "strokeWidth");

                  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                  path.setAttribute("d", "M 0 0 L 10 5 L 0 10 Z");
                  path.setAttribute("fill", "black");

                  marker.appendChild(path);
                  defs.appendChild(marker);
                  svg.appendChild(defs);
                }

              console.log(svg);
              const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
              line.id = `line-${taskId}`;
              line.setAttribute("x1", Number(width0 / 2) + Number(x0) );
              line.setAttribute("y1", Number(y0) + Number(height0 / 2));
              line.setAttribute("x2", Number(x1) + Number(width1 / 2));
              line.setAttribute("y2", Number(y1)  + Number(height1 / 2));
              line.setAttribute("stroke", "red");
              line.setAttribute("stroke-width", "4");
              line.setAttribute("marker-end", "url(#arrow)");
              svg.appendChild(line);
            }





          
        },
        setupWebSocket() {
                  const wsUrl = `ws://${window.location.hostname}:5001/crane22/ws`
                  console.log("try to connect crane");
                  this.ws = new WebSocket(wsUrl);


                  this.ws.onmessage = (event) => {
                      try {
                        const task = JSON.parse(event.data);
                        this.tasks.push(task);
                        this.taskAdd(task);
                      }
                      catch (err){
                        console.error("Ошибка обработки WS-сообщения:", err);
                      }

                  }
                  this.ws.onopen = function(event) {
                      console.log(event)
                      console.log("Подключен к websocket серверу")
                  }
                  this.ws.onerror = function(event){
                      console.log(event);
                      alert("Не получилось соединиться с сервером, пожалуйста, перезагрузите страницу. Если перезагрузка не помогла, то сообщите об этой проблеме администратору")

                  }
        },
        async choiceAcceptTask(taskId){
          
          //this.isModalOpen = true;
          // openModal(this.isModalOpen);
        },

        async acceptTask(taskId) {

                  await this.choiceAcceptTask(taskId);
                  
                  try {
                    const response = await axios.post(`http://localhost:5001/task/accept?task_id=${taskId}`);

                    console.log(`✅ Задача ${taskId} теперь в состоянии ${response.data.state}`);

                    if( response.data.state === "in_progress"){
                        const td = document.getElementById(`state-${taskId}`);
                        td.innerText = "in progress";
                        const btn = document.getElementById(`start-${taskId}`);
                        const newBtn = btn.cloneNode(true);
                        btn.parentNode.replaceChild(newBtn, btn);

                        
                        newBtn.id = `stop-${taskId}`;
                        newBtn.textContent = "Закончить";
                        newBtn.addEventListener("click", () => this.taskComplete(taskId));



                        
                        let task = null;
                        for (let i = 0; i < this.tasks.length; i++){
                          console.log(this.tasks[i])
                            if (this.tasks[i].id == taskId){
                              task = this.tasks[i];
                              break;
                            }
                        }
                        console.log(`Задание ${task}`);
                        
                        const from_ = document.getElementById(`place-${task.from_id}`);
                        const to = document.getElementById(`place-${task.to_id}`);

                        const x0 = from_.getAttribute("x");
                        const y0 = from_.getAttribute("y");

                        const width0 = from_.getAttribute("width");
                        const height0 = from_.getAttribute("height");

                        const x1 = to.getAttribute("x");
                        const y1 = to.getAttribute("y");

                        const width1 = to.getAttribute("width");
                        const height1 = to.getAttribute("height");


                        const svg = document.querySelector("svg");
                        if (!document.getElementById("arrow")) {
                            const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
                            const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");

                            marker.id = "arrow";
                            marker.setAttribute("markerWidth", "10");
                            marker.setAttribute("markerHeight", "10");
                            marker.setAttribute("refX", "9");
                            marker.setAttribute("refY", "5");
                            marker.setAttribute("orient", "auto");
                            marker.setAttribute("markerUnits", "strokeWidth");

                            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                            path.setAttribute("d", "M 0 0 L 10 5 L 0 10 Z");
                            path.setAttribute("fill", "black");

                            marker.appendChild(path);
                            defs.appendChild(marker);
                            svg.appendChild(defs);
                          }

                        console.log(svg);
                        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line.id = `line-${taskId}`;
                        line.setAttribute("x1", Number(width0 / 2) + Number(x0) );
                        line.setAttribute("y1", Number(y0) + Number(height0 / 2));
                        line.setAttribute("x2", Number(x1) + Number(width1 / 2));
                        line.setAttribute("y2", Number(y1)  + Number(height1 / 2));
                        line.setAttribute("stroke", "red");
                        line.setAttribute("stroke-width", "4");
                        line.setAttribute("marker-end", "url(#arrow)");

                        svg.appendChild(line);


                        console.log(from_);
                        console.log(to);
                        console.log(task);

                    }
                    console.log(response.data);
                  } catch (error) {
                    console.error("Ошибка запроса:", error.response ? error.response.data : error.message);
                  }

        },
        taskAdd(task){
            if (task.state == 2)
              return;
            if (task.state == 0){
              const tableBody = document.getElementById("tasks_table");
              const row = document.createElement("tr");
              row.id = `task-${task.id}`;
              
              row.innerHTML = `
              <td>#${task.id}</td> 
              <td><button id="start-${task.id}">Начать</button></td>
              <td id='state-${task.id}'> ${task.state == 0? "not start": "in progress"} </td>`;
              
              tableBody.appendChild(row);
              document.getElementById(`start-${task.id}`).addEventListener("click", () => this.acceptTask(task.id));
            }  
            else if (task.state == 1){
              this.drawTask(task);
              const tableBody = document.getElementById("tasks_table");
              const row = document.createElement("tr");
              row.id = `task-${task.id}`;
              
              row.innerHTML = `
              <td>#${task.id}</td> 
              <td><button id="stop-${task.id}">Закончить</button></td>
              <td id='state-${task.id}'> ${task.state == 0? "not start": "in progress"} </td>`;

              tableBody.appendChild(row);
              console.log(task);
              const btn = document.getElementById(`stop-${task.id}`);

              btn.addEventListener("click", () => this.taskComplete(task.id));
            }

            


        },

        

        async taskComplete(taskId){
          console.log(`Закончил таску ${taskId}`);


          try {
                    const response = await axios.post(`http://localhost:5001/task/complete?task_id=${taskId}`);

                    console.log(`✅ Задача ${taskId} теперь в состоянии ${response.data.state}`);

                    if( response.data.state === "completed"){
                        const task_row = document.getElementById(`task-${taskId}`);
                        task_row.remove();
                        const line_task = document.getElementById(`line-${taskId}`);
                        line_task.remove();
                    }
                    console.log(response.data);
                  } catch (error) {
                    console.error("Ошибка запроса:", error.response ? error.response.data : error.message);
                  }
        },

        taskInProcess(id){

        },

        
      },
      mounted() {

              
              //Вот тут начинаем строить
              const workZone = document.querySelector(".work_zone");

        
            
              const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
              svg.id = 'svg';
              svg.setAttribute("width", "100%");
              svg.setAttribute("height", "100%");
              workZone.appendChild(svg);
              


              const Width = workZone.clientWidth - 5;
              const Height = workZone.clientHeight - 5;

              (async () => {
                        const response = await fetch("http://localhost:5001/crane22/work_zone");
                        const data = await response.json();
                        console.log("✅ Данные получены:", data);


                        // отрисовка зон
                        data['zones'].forEach(zone => {

                              const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                              //rect.id = `zone-${zone.id}`; //
                              rect.setAttribute("x", zone.poss[0] * Width);
                              rect.setAttribute("y", zone.poss[1] * Height);
                              rect.setAttribute("width", zone.width* Width);
                              rect.setAttribute("height", zone.height * Height);
                              rect.setAttribute("fill", "gray");
                              rect.setAttribute("stroke", "black");
                              rect.setAttribute("stroke-width", "2");
                              svg.appendChild(rect);

                              zone["places"].forEach(place => {

                                  const rect_place = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                                  rect_place.id = `place-${place.id}`;

                                  rect_place.setAttribute("x", zone.poss[0] * Width + place.poss[0] * Width);
                                  rect_place.setAttribute("y", zone.poss[1] * Height + place.poss[1] * Height);
                                  rect_place.setAttribute("width", place.width * Width);
                                  rect_place.setAttribute("height", place.height * Height);
                                  rect_place.setAttribute("fill", "yellow");
                                  rect_place.setAttribute("stroke", "black");
                                  rect_place.setAttribute("stroke-width", "2");
                                  svg.appendChild(rect_place);

                                  console.log("построил");

                              })

                        });


              })();

              console.log(workZone.clientHeight);
              this.setupWebSocket();
      }
    }


</script>

<template>

        <div class="container">

          <div v-if="isOpen" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
                <span class="close-btn" @click="closeModal">&times;</span>
                <h2 id="number-task"></h2>
                <p id="count-list"><strong>Кол-во листов:</strong> </p>
                <p id="from"><strong>Откуда:</strong></p>
                <p id="to"><strong>Куда:</strong></p>
                <p id="comment">Комментарий</p>

                <div class="buttons">
                  <button class="accept" @click="acceptTaskState">Принять</button>
                  <button class="decline" @click="declineTaskState">Отклонить</button>
                </div>
            </div>
          </div>

          <div class="task_zone">
            
              <table>
                <thead>
                  <td>Номер задания</td>
                  <td>Действие</td>
                  <td>Статус</td>
                </thead>
              <tbody id="tasks_table">
                    <!-- Тут у нас по websocket забирает таски-->

              </tbody>

              </table>
          </div>




          <div class="work_zone">
          </div>
        </div>


</template>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Контейнер модального окна */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 350px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

/* Кнопка закрытия */
.close-btn {
  float: right;
  font-size: 24px;
  cursor: pointer;
}

.close-btn:hover {
  color: red;
}

/* Кнопки действий */
.buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.accept {
  background: green;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.decline {
  background: red;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.accept:hover {
  background: darkgreen;
}

.decline:hover {
  background: darkred;
}
.open-btn {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

/* Задний фон модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Само модальное окно */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 300px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

/* Кнопка закрытия */
.close-btn {
  float: right;
  font-size: 24px;
  cursor: pointer;
}

.close-btn:hover {
  color: red;
}

    html, body {
      margin: 0; 
      padding: 0; 
      height: 100%;
      box-sizing: border-box;
    }
    .container {
      display: flex;       /* Включаем flex */
      width: 100vw;        /* На всю ширину экрана */
      height: 100vh;       /* На всю высоту экрана */
    }
    .task_zone {
      flex: 1;             /* Левая колонка = 1 часть */
      border-right: 2px solid #333; /* Вертикальная черта */
      box-sizing: border-box;
      overflow: auto;
      /* Для наглядности можно добавить фон */
      background-color: rgba(255,0,0,0.1);
    }
    .work_zone {
      flex: 4.5; 
      overflow: hidden;            /* Правая колонка = 7 частей */
      box-sizing: border-box;
      background-color: rgba(0,0,255,0.1);
    }


    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 5px;
      
}

th, td {
  border: 1px solid #ccc;
  padding: 4px;
  font-size: 12px;
  text-align: left;
  word-wrap: break-word;

}

th {
  background-color: #f4f4f4;
}


/* Общий стиль для Chrome, Safari, Edge */
::-webkit-scrollbar {
  width: 10px; /* Толщина скроллбара */
}

/* Фон полосы прокрутки */
::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 5px;
}

/* Сам ползунок */
::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #ff6b6b, #ffb88c); /* Градиент */
  border-radius: 5px;
}

/* При наведении */
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #ff3b3b, #ff914d);
}

/* Для Firefox */
* {
  scrollbar-width: thin; /* Тонкий скролл */
  scrollbar-color: #ff6b6b #f0f0f0; /* (Цвет ползунка, цвет фона) */
}

  </style>
