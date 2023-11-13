const http = require('http');
const url = require('url');
const express = require('express');
const exp = require('constants');
const swaggerUI = require('swagger-ui-express');
const swaggerJsDoc = require('swagger-jsdoc');
const YAML = require('yamljs')
const apiRouter = require("./routes/virtualAPI")
const cors = require('cors');

const fs = require('fs');
const jsYaml = require('js-yaml');

// port randomly assigned during deployment so use process.env.port 
const PORT = process.env.PORT || 3030; 
// const swaggerUI = require("swagger-ui-express")
// const swaggerJsDoc = require("swagger-jsdoc")

// const bodyParser = require('body-parser');

// import { spawn } from 'child_process';



const options = {
    definition:{
        openapi:"3.0.0",
        info:{
            title:"Virtual Agent Power BI API",
            version:"1.0.0",
            description:"API to connect use Open AI with Virtual Aggent"
        },
       
        
    },
    apis:["./routes/*.js"]
}

const specs = swaggerJsDoc(options)

const yamlData = jsYaml.dump(specs);

// fs.writeFile('swagger.yaml', yamlData, (err) => {
//     if (err) {
//       console.error('Error writing YAML file:', err);
//     } else {
//       console.log('Swagger YAML file generated as "swagger.yaml".');
//     }
//   });

// const jsonContent = JSON.stringify(specs, null, 2); // Convert the Swagger object to JSON

// fs.writeFile('swaggerMy.json', jsonContent, (err) => {
//   if (err) {
//     console.error('Error writing JSON file:', err);
//   } else {
//     console.log('Swagger JSON file generated as "swagger.json".');
//   }
// });
  

const app = express()
app.use(express.json())
app.use(cors());
app.use("/api-docs",swaggerUI.serve,swaggerUI.setup(specs))
app.use("/",apiRouter)


app.listen(PORT , () => {
  console.log(`Server is running on port ${PORT}`);
});
