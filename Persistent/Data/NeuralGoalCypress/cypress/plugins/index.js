/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)
const fs = require('fs')
var obj = {}
obj.table = []


var GameMatch = {}
GameMatch.table = []

/**
 * @type {Cypress.PluginConfig}
 */
module.exports = (on, config) => {

  on('task', {
    addAttribute(elementToAdd) {
      GameMatch.table.push(elementToAdd)
      return null
    }
  })

  on('task', {
    addMatch () {
      obj.table.push(GameMatch.table);
      GameMatch = {}
      GameMatch.table = []
      return null
    }
  })

  on('task', {
    saveJson (jsonName) {
      let path = 'C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\Prediction\\myJson.json'
      fs.writeFile(path.replace(new RegExp('myJson',"g"),jsonName), JSON.stringify(obj), 'utf8');
      obj = {}
      obj.table = []
      return null
    }
  })
}

