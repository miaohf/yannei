const getters = {
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  userId: state => state.user.userId,
  name: state => state.user.name,
  introduction: state => state.user.introduction,
  role: state => state.user.role,
  permission_routes: state => state.permission.routes,
}
export default getters
