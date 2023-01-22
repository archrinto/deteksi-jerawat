
<template>
  <v-app id="inspire">

    <v-app-bar color="primary" flat dark app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-toolbar flat color="primary">
        <!-- <v-btn
          icon
          class="hidden-xs-only white--text"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn> -->

        <v-toolbar-title class="text-h6 white--text">
          Skin Analyzer
        </v-toolbar-title>
      </v-toolbar>

      <v-divider></v-divider>

      <!-- <v-list>
        <v-list-item link>
          <v-list-item-avatar>
            <v-img src="https://cdn.vuetifyjs.com/images/john.png"></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="text-h6">
              John Leider
            </v-list-item-title>
            <v-list-item-subtitle>john@vuetifyjs.com</v-list-item-subtitle>
          </v-list-item-content>

        </v-list-item>
      </v-list> 
      
      <v-divider></v-divider>
      -->


      <v-list class="pt-0">
        <v-list-item link @click="openDialogAsesmen">
          <v-list-item-icon>
            <v-icon>mdi-camera</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Asesmen</v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>
      </v-list>

      <v-list>
        <v-list-item-group color="primary">
          <v-list-group
            no-action
            :value="true"
            prepend-icon="mdi-face-recognition"
            color="primary"
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Gambar</v-list-item-title>
              </v-list-item-content>
            </template>

              <!-- <v-list-item link>
                <v-list-item-title>Overview</v-list-item-title>
              </v-list-item> -->

              <v-list-item to="/jerawat" link>
                <v-list-item-title>Jerawat</v-list-item-title>
              </v-list-item>
              <v-list-item to="/bintik-hitam" link>
                <v-list-item-title>Bintik Hitam</v-list-item-title>
              </v-list-item>
              <v-list-item to="/kemerahan" link>
                <v-list-item-title>Kemerahan</v-list-item-title>
              </v-list-item>
              <v-list-item to="/keriput" link>
                <v-list-item-title>Keriput</v-list-item-title>
              </v-list-item>
          </v-list-group>

          <v-list-item to="/debugging" link>
            <v-list-item-icon>
              <v-icon>mdi-bug</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Debugging</v-list-item-title>
          </v-list-item>

          <!-- <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-printer</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Reports</v-list-item-title>
          </v-list-item> -->

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container
        class="py-3 px-3"
        fluid
      >
        <router-view 
          :client-id="clientId" 
          :images="images" 
          :results="results" 
          @openDialogAsesmen="openDialogAsesmen"
        ></router-view>

      </v-container>
    </v-main>

<!-- DIALOG ASESMEN -->
    <v-dialog
      v-model="isDialogAsesmen"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :loading="isLoading">
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="closeDialogAsesmen"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Ambil Foto</v-toolbar-title>
          <v-spacer></v-spacer>

          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="uploadImage"
              :loading="isLoading"
            >
              Analisis
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        
        <v-slide-group
          class="pa-2"
          center-active
          show-arrows
        >
          <v-spacer></v-spacer>
          <v-slide-item
            v-for="(img, n) in imageList"
            :key="n"
          >
            <v-card
              :color="selectedImageIndex == n ? 'primary' : 'grey lighten-1'"
              class="ma-4"
              height="100"
              width="100"
              @click="selectedImageIndex = n"
            >
              <v-img :src="img" max-height="100%"></v-img>
            </v-card>
          </v-slide-item>

          <v-slide-item>
            <v-btn 
              class="ma-4"
              height="100"
              width="100"
              text
              @click="addImage"
            >
              <v-row
                class="fill-height"
                align="center"
                justify="center"
              >
                <v-scale-transition>
                  <v-icon
                    color="primary"
                    size="40"
                    v-text="'mdi-plus'"
                  ></v-icon>
                </v-scale-transition>
              </v-row>
            </v-btn>
          </v-slide-item>
          <v-spacer></v-spacer>
        </v-slide-group>


        <div class="text-center pa-2">
          <v-row justify="center">
            <v-col md="4" align-self="center">
              <v-img max-width="100%" v-if="selectedImageIndex != null" :src="imageList[selectedImageIndex]"></v-img>
            </v-col>
          </v-row>
        </div>

      </v-card>
    </v-dialog>
<!-- END DIALOG ASESMEN -->

<!-- DIALOG CAMERA -->
    <v-dialog
      v-model="isDialogCamera"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :loading="isLoading">
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="closeDialogCamera"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Camera</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="addImageList"
              :disabled="isCameraOpen"
              :loading="isLoading"
            >
              Tambah
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <div class="text-center pa-2">
          <v-row justify="center">
            <v-col md="5" align-self="center">
              <div class="text-center mb-4">
                <center>
                  <v-select
                    v-model="selectedCamera"
                    :items="listCamera"
                    menu-props="auto"
                    hide-details
                    prepend-icon="mdi-camera"
                    single-line
                    @change="onCameraChange"
                    :disabled="!isCameraOpen"
                  ></v-select>
                </center>

              </div>
              <v-img v-show="!isCameraOpen" max-width="100%" :src="selectedFile"></v-img>
              <video v-show="isCameraOpen" ref="camera" autoplay width="100%"></video>
              <canvas style="display: none;" id="photoTaken" ref="canvas" width="100%"></canvas>

              <div class="text-center mt-4">
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  color="primary"
                  :disabled="!isCameraOpen"
                  @click="takePhoto"
                >
                  <v-icon dark>
                    mdi-camera
                  </v-icon>
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </div>
      
      </v-card>
    </v-dialog>
<!-- END DIALOG KAMERA -->
<!-- DIALOG FILE -->
    <v-dialog
      v-model="isDialogFile"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :loading="isLoading">
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="closeDialogFile"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>File</v-toolbar-title>
          <v-spacer></v-spacer>          
          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="addImageList"
              :loading="isLoading"
            >
              Tambah
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        
        <input style="display: none" ref="fileImage" type="file" @change="onFileChange" accept="image/*" enctype="multipart/form-data">
        
        <div class="text-center pa-2">
          <v-row justify="center">
            <v-col md="4" align-self="center">
              <v-img max-width="100%" :src="selectedFile"></v-img>
            </v-col>
          </v-row>
        </div>

      </v-card>
    </v-dialog>
<!-- END DIALOG FILE -->
<!-- DIALOG HASIL -->
    <v-dialog
      v-model="isDialogHasil"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :loading="isLoading">
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="closeDialogHasil"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Hasil Deteksi Jerawat</v-toolbar-title>
          <v-spacer></v-spacer>          
        </v-toolbar>
        
        <div v-if="imageList.length > 0">
          <v-slide-group
            class="pa-2"
            center-active
            show-arrows
          >
            <v-spacer></v-spacer>

            <v-slide-item
              v-for="(img, n) in imageList"
              :key="n"
            >
              <v-card
                :color="selectedImageIndex == n ? 'primary' : 'grey lighten-1'"
                class="ma-4"
                height="100"
                width="100"
                @click="selectedImageIndex = n"
              >
                <v-img :src="img"></v-img>
              </v-card>
            </v-slide-item>

            <v-spacer></v-spacer>
          </v-slide-group>
          <div class="text-center pa-2">
            <v-row justify="center">
              <v-col md="4" align-self="center">
                Jumlah: {{ jumlahTerdeteksi }} jerawat
              </v-col>
            </v-row>
            <v-row justify="center">
              <v-col md="4" align-self="center">
                <canvas id="renderHasil" ref="display" width="100%"></canvas>
                <!-- <v-img max-width="100%" v-if="selectedImageIndex != null" :src="imageList[selectedImageIndex]"></v-img> -->
              </v-col>
            </v-row>
          </div>
        </div>
      </v-card>
    </v-dialog>
<!-- END DIALOG HASIL -->

    <v-bottom-sheet v-model="isSelectSource">
      <v-sheet
        class="text-center"
        height="200px"
      >
        <div class="text-center text-caption py-4">Pilih sumber foto</div>
        
        <div class="py-3">
          <v-btn
            class="mx-4"
            fab
            @click="openDialogFile"
          >
            <v-icon>mdi-folder-open</v-icon>
          </v-btn>
          <v-btn
            class="mx-4"
            fab
            @click="openDialogCamera"
          >
            <v-icon>mdi-camera</v-icon>
          </v-btn>
        </div>
      </v-sheet>
    </v-bottom-sheet>

  </v-app>
</template>

<script>
  export default {
    mounted() {
      // this.clientCheckin()
      // setTimeout(() => {
      //   this.imageAnalysis()
      // }, 1000)
    },
    watch: {
      selectedImageIndex: function(val) {
        if (val != 'undefined') {
          if (!this.isDialogHasil) {
            if (this.images[val] && this.images[val].src) {
              this.selectedImage = this.images[val]
            } else {
              if (val != null) {
                this.openSelectSource()
              }
            }
          } else {
            this.changeImage()
          }
        }
        // console.log(this.selectedImage)
        this.selectedImage = null
      }
    },
    data: () => ({
      images: [
        { src: null }
      ],
      selectedImage: null,
      clientId: null,
      selectedFile: null,
      selectedImageIndex: null,
      isDialogAsesmen: false,
      isDialogCamera: false,
      isDialogFile: false,
      selectedItem: null,
      selectedItemMenu: null,
      isSelectSource: false,
      listCamera: [],
      selectedCamera: null,
      isDialogHasil: false,
      jumlahTerdeteksi: 0,
      // menampung data gambar
      imageList: [],
      cards: ['Today', 'Yesterday'],
      drawer: null,
      links: [
        ['mdi-inbox-arrow-down', 'Inbox'],
        ['mdi-send', 'Send'],
        ['mdi-delete', 'Trash'],
        ['mdi-alert-octagon', 'Spam'],
      ],
      isCameraOpen: false,
      isPhotoTaken: false,
      isShotPhoto: false,
      isLoading: false,
      results: [],
      link: '#'
    }),
    methods: {
      async getUserMediaDevice() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
          console.log("enumerateDevices() not supported.");
          return
        }

        // List cameras and microphones.
        const listDevice = []
        await navigator.mediaDevices.enumerateDevices()
        .then(function(devices) {
          devices.forEach(function(device) {
            if (device.kind == 'videoinput') {
              listDevice.push(
                { value: device.deviceId, text: device.label}
              )
            }
          });
        })
        .catch(function(err) {
          console.log(err.name + ": " + err.message);
        })
        this.listCamera = listDevice
        if (listDevice.length > 0) {
          this.selectedCamera = listDevice[0]
        }
      },
      clientCheckin() {
        this.$axios.get('/api/checkin')
        .then(res => {
          this.clientId = res.data.client_id
          // console.log(res.data.client_id)
          // this.clientId = '25ba507a-7953-4b0b-a02b-0eff0459df97'
          this.$axios.defaults.headers.common['Client-Id'] = this.clientId
          window.axios.defaults.headers.common['Client-Id'] = this.clientId
        })
      },
      openDialogAsesmen() {
        this.isDialogAsesmen = true
        setTimeout(() => {
          this.selectedImageIndex = 0
        }, 500)
      }, 
      closeDialogAsesmen() {
        this.selectedImageIndex = null
        this.isDialogAsesmen = false
      },
      openDialogHasil() {
        this.selectedImageIndex = 0
        this.isDialogHasil = true

        setTimeout(() => {
          this.changeImage()
        }, 1000)
      }, 
      closeDialogHasil() {
        this.imageList = []
        this.selectedImageIndex = null
        this.results = []
        this.isDialogHasil = false
      },
      openSelectSource() {
        this.isSelectSource = true
      },
      closeSelectSource() {
        this.isSelectSource = false
      },
      async openDialogCamera() {
        this.isDialogCamera = true
        await this.getUserMediaDevice()
        setTimeout(() => {
          this.openCamera()
        }, 1000)
      },
      closeDialogCamera() {
        this.closeCamera()
        this.isDialogCamera = false
      },
      openDialogFile() {
        this.isDialogFile = true
        setTimeout(() => {
          this.$refs.fileImage.click()
        }, 500)
      },
      addImage() {
        this.images.push({ src: null })
        setTimeout(() => {
          this.selectedImageIndex = this.images.length - 1
        }, 500)
      },
      closeDialogFile() {
        this.isDialogFile = false
      },
      async onFileChange(e) {
        const toBase64 = file => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
        this.selectedFile = await toBase64(e.target.files[0]);
      },
      openCamera() {
        this.isCameraOpen = true;
        this.createCameraElement();
      },
      closeCamera() {
        if (this.isCameraOpen) {
          this.isCameraOpen = false;
          this.isShotPhoto = false;
          this.stopCameraStream();
        }
      },
        
      createCameraElement() {
        this.isLoading = true;
        
        let video = true
        if (this.selectedCamera) {
          video = { deviceId: this.selectedCamera.value}
        }

        const constraints = (window.constraints = {
          audio: false,
          video: video
        });

        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(stream => {
            this.isLoading = false;
            this.$refs.camera.srcObject = stream;
          })
          .catch(error => {
            console.log(error)
            this.isLoading = false;
            alert("May the browser didn't support or there is some errors.");
          });
      },
      
      stopCameraStream() {
        let tracks = this.$refs.camera.srcObject.getTracks();

        tracks.forEach(track => {
          track.stop();
        });
      },
      
      takePhoto() {
        if(!this.isPhotoTaken) {
          this.isShotPhoto = true;

          const FLASH_TIMEOUT = 50;

          setTimeout(() => {
            this.isShotPhoto = false;
          }, FLASH_TIMEOUT);
        }
        
        // this.isPhotoTaken = !this.isPhotoTaken;
        
        this.$refs.canvas.width = this.$refs.camera.videoWidth
        this.$refs.canvas.height = this.$refs.camera.videoHeight
        const context = this.$refs.canvas.getContext('2d');
        context.drawImage(this.$refs.camera, 0, 0, this.$refs.camera.videoWidth, this.$refs.camera.videoHeight);

        this.selectedFile = this.$refs.canvas.toDataURL("image/jpeg")

        this.closeCamera()
      },
      
      downloadImage() {
        const download = document.getElementById("downloadPhoto");
        const canvas = document.getElementById("photoTaken").toDataURL("image/jpeg")
      .replace("image/jpeg", "image/octet-stream");
        download.setAttribute("href", canvas);
      },

      onCameraChange() {
        this.closeCamera()
        setTimeout(() => {
          this.openCamera()
        }, 1000)
      },

      async addImageList() {
        this.imageList.push(this.selectedFile)
        this.selectedFile = null
        // console.log(this.selectedFile);

        setTimeout(() => {
          this.closeDialogCamera()
          this.closeDialogFile()
          this.closeSelectSource()
        }, 1000)
      },

      // Upload image
      async uploadImage() {
        this.isLoading = true
        const formData = new FormData();
        this.imageList.forEach(element => {
          const blobBin = atob(element.split(',')[1]);
          const array = [];
          for(var i = 0; i < blobBin.length; i++) {
              array.push(blobBin.charCodeAt(i));
          }

          const file = new Blob([new Uint8Array(array)], {type: 'image/jpeg'});

          formData.append('file[]', file)
        });
        
        const config = {
          headers: {
            "content-type": "multipart/form-data"
          }
        }
        await this.$axios.post('/api/deteksi_keriput', formData, config)
        .then(res => {
          this.results = res.data
        })

        this.isLoading = false

        setTimeout(() => {
          this.closeDialogAsesmen()
          this.openDialogHasil()
        }, 1000)

        // this.selectedFile = null
      },

      async imageAnalysis() {
        this.isLoading = true
        const results = await this.$axios.get('/api/skin_analysis')
        .then(res => {
          return res.data
        }).catch(err => {
          console.log(err)
          return []
        })
        
        this.isLoading = false
        this.results = results
        setTimeout(() => {
          this.closeDialogAsesmen()
          this.$router.push('/keriput')
        }, 1000)
      },

      async changeImage() {
        if (this.results.length == 0) {
          return
        }

        const result = this.results[this.selectedImageIndex]
        this.currentResult = result

        let items = []
        this.jumlahTerdeteksi = 0
        if (this.currentResult != null && this.currentResult.deteksi_objek.keriput) {
          items = this.currentResult.deteksi_objek.keriput
          this.jumlahTerdeteksi = items.length
        }
        
        const image = new Image()
        const canvas = document.getElementById('renderHasil')
        const context = canvas.getContext('2d')

        context.clearRect(0, 0, canvas.width, canvas.height);

        image.onload = function() {
          console.log('loaded')

          canvas.style.width = '100%'

          let { width, height } = canvas.getBoundingClientRect();
          
          height = (width / image.width) * image.height

          height = image.height
          width = image.width

          canvas.width = width
          canvas.height = height

          context.drawImage(image, 0, 0, width, height)
          
          items.forEach(item => {
            const ymin = item.ymin, xmin = item.xmin, ymax = item.ymax, xmax = item.xmax
            const left = xmin * width
            const right = xmax * width
            const top = ymin * height
            const bottom = ymax * height
            const box_h = bottom-top, box_w = right-left
            // let radius = Math.sqrt((box_h) ** 2 + (box_w) ** 2) / 2
            
            context.strokeStyle = "yellow"

            context.beginPath();
            context.strokeRect(left, top, right-left, bottom-top);
            // context.arc(left + box_w / 2, top + box_h / 2, radius, 0, 2 * Math.PI);
            context.stroke();
          });
        }
        image.src = this.imageList[this.selectedImageIndex]
      }
    },
  }
</script>