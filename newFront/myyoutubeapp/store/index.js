export const state = () => ({
  counter: 1,
  token: 'v',
  list: [],
  car: {}
})
  
export const mutations = {
  increment (state) {
    state.counter++
  },
  updateToken (state, token) {
    state.token = token
  }
}