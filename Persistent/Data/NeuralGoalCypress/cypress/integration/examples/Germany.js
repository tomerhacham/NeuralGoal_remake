
context('Get Data', () => {
  it('Get games from Winner',() =>{
    let siteUrl = 'https://www.winner.co.il/mainbook/sport-%D7%9B%D7%93%D7%95%D7%A8%D7%92%D7%9C/ep-%D7%92%D7%A8%D7%9E%D7%A0%D7%99%D7%94/ep-%D7%92%D7%A8%D7%9E%D7%A0%D7%99%D7%AA-%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%94?date=all&marketTypePeriod=1%7C100'
    cy.visit(siteUrl)
      cy.get('.event_path-content').children().its('length').then((length) => {
        for(let j = 0 ; j < length; j++){
          cy.get('.event_path-content').children().eq(j).find('.event').find('td').eq(2).find('tr').find('td').eq(0).find('.pseudotable').find('.title').find('span').eq(0).invoke('text').then((teamsName) => {
            cy.task('addAttribute',{'HomeTeam':teamsName})
          })
          cy.get('.event_path-content').children().eq(j).find('.event').find('td').eq(2).find('tr').find('td').eq(2).find('.pseudotable').find('.title').find('span').eq(0).invoke('text').then((awayTeamName) => {
            cy.task('addAttribute',{'AwayTeam':awayTeamName})
          })
          cy.get('.event_path-content').children().eq(j).find('.event').find('td').eq(2).find('tr').find('td').eq(0).find('.pseudotable').find('.title').find('span').eq(1).find('span').invoke('text').then((homeTeamOdds) => {
            cy.task('addAttribute',{'HomeTeamOdds':homeTeamOdds})
          })
          cy.get('.event_path-content').children().eq(j).find('.event').find('td').eq(2).find('tr').find('td').eq(1).find('.pseudotable').find('.title').find('span').eq(1).find('span').invoke('text').then((drawOdds) => {
            cy.task('addAttribute',{'DrawOdds':drawOdds})
          })
          cy.get('.event_path-content').children().eq(j).find('.event').find('td').eq(2).find('tr').find('td').eq(2).find('.pseudotable').find('.title').find('span').eq(1).find('span').invoke('text').then((awayTaemOdds) => {
            cy.task('addAttribute',{'AwayTeamOdds':awayTaemOdds})
          })
          cy.task('addMatch')
        }
        cy.task('saveJson','BundesligaWinner')
      })
  })
})