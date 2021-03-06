<template>
    <div>
        Hello world!
    </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  width: 100vw;
  min-width: 300px;
  max-width: 1000px;
  margin: 0 auto;
}
.commands {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 20px;
  justify-content: center;
}
h2 {
  margin: 10px;
}
form {
  margin: 20px;
  display: flex;
  flex-direction: column;
}
form textarea {
  resize: none;
  height: 30px;
  margin: 0 10px 10px;
  background: beige;
  outline: none !important;
  border: none;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
  border-radius: 5px;
  padding: 10px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 1em;
}
form button {
  background: lightgreen;
  color: darkgreen;
  padding: 10px;
  border: none;
  border-radius: 5px;
  margin: 10px;
  cursor: pointer;
  outline: none !important;
}
form button:hover {
  background-color: #a0fea0;
}
</style>
