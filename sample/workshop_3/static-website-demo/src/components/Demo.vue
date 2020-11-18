<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <span for="jwtSecretInput">Your JWT Secret : </span>
    <input
      id="jwtSecretInput"
      v-model="jwtSecret"
      placeholder="JWT Secret"
      :type="jwtSecretType"
    />
    <br />
    <div style="margin-top: 15px; margin-bottom: 10px">
      <span> show secret </span>
      <label class="switch">
        <input type="checkbox" v-model="showSecret" />
        <span class="slider round"></span>
      </label>
    </div>

    <button @click="userPaper()" style="margin-left: 10px">Paper</button>
    <button @click="userRock()" style="margin-left: 10px">Rock</button>
    <button @click="userScissors()" style="margin-left: 10px">Scissors</button>
    <div v-if="!errorMsg">
      <p>{{ userMsg }}</p>
      <img :src="userImgUrl" />
      <h1 v-if="userImgUrl">VS</h1>
      <img :src="computerImgUrl" />
      <p>{{ computerMsg }}</p>
    </div>
    <div v-else>
      <h1 style="color: red">{{ errorMsg }}</h1>
    </div>
  </div>
</template>

<script>
import KJUR from "jsrsasign";

const vueData = {
  data() {
    return {
      userMsg: "",
      computerMsg: "",
      jwtSecret: "",
      showSecret: false,
      userImgUrl: null,
      computerImgUrl: null,
      errorMsg: ""
    };
  }
};

export default {
  name: "HelloWorld",
  props: {
    msg: String
  },
  mixins: [vueData],
  computed: {
    jwtSecretType() {
      if (this.showSecret) return "text";
      return "password";
    }
  },
  methods: {
    computerRandom() {
      const picArr = ["paper", "rock", "scissors"];
      const randomPic = picArr[Math.floor(Math.random() * picArr.length)];
      this.getPicture(randomPic, false);
      this.computerMsg = "computer choose " + randomPic;
    },
    userPaper() {
      this.userMsg = "you choose paper";
      this.getPicture("paper", true);
      this.computerRandom();
    },
    userRock() {
      this.userMsg = "you choose rock";
      this.getPicture("rock", true);
      this.computerRandom();
    },
    userScissors() {
      this.userMsg = "you choose scissors";
      this.getPicture("scissors", true);
      this.computerRandom();
    },
    getPicture(fileName, userFlag) {
      const oHeader = { alg: "HS256" };
      const sHeader = JSON.stringify(oHeader);
      const sPayload = { sub: "lambda-edge-demo" };

      const sJWS = KJUR.jws.JWS.sign(
        "HS256",
        sHeader,
        sPayload,
        this.jwtSecret
      );

      this.axios
        .get(`${fileName}.png`, {
          responseType: "arraybuffer",
          headers: {
            Authorization: "Bearer " + sJWS,
            'Cache-Control': 'no-cache',
            Pragma: 'no-cache',
            Expires: 0,
          }
        })
        .then(response => {
          return (
            "data:image/png;base64," +
            btoa(
              new Uint8Array(response.data).reduce(
                (data, byte) => data + String.fromCharCode(byte),
                ""
              )
            )
          );
        })
        .then(data => {
          if (userFlag) {
            this.userImgUrl = data;
          } else {
            this.computerImgUrl = data;
          }
          this.errorMsg = '';
        })
        .catch(error => {
          this.errorMsg = error;
        });
    }
  }
};
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
/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  bottom: 5px;
  margin-left: 10px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #2196f3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196f3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
