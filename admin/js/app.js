Vue.component("pager", {
  props: ["state"],
  template:
    '<div class="pager"><el-pagination background layout="total, sizes, prev, pager, next" :current-page="state.page" :page-size="state.page_size" :page-sizes="[10,20,50,100]" :total="state.total" @size-change="size => $emit(\'change\', { page: 1, page_size: size })" @current-change="page => $emit(\'change\', { page: page, page_size: state.page_size })"></el-pagination></div>',
});

const emptyPage = () => ({ items: [], page: 1, page_size: 10, total: 0, has_more: false });
const splitList = (value) =>
  String(value || "")
    .split(/[,，\n]/)
    .map((item) => item.trim())
    .filter(Boolean);

new Vue({
  el: "#app",
  data() {
    return {
      token: localStorage.getItem("admin_token") || "",
      currentUser: localStorage.getItem("admin_username") || "",
      apiBase: localStorage.getItem("admin_api_base") || "http://127.0.0.1:8000/api/v1",
      active: localStorage.getItem("admin_active") || "dashboard",
      loading: { login: false },
      loginForm: { username: "admin", password: "admin123456" },
      dashboard: { counts: {}, hot_poems: [], latest_topics: [], feedback_status: {}, trend: [] },
      categories: [],
      filters: {
        poems: { keyword: "", dynasty: "", author: "" },
        users: { keyword: "" },
        topics: { keyword: "", user_id: undefined },
        comments: { keyword: "", topic_id: undefined },
        feedback: { status: "" },
        rooms: { keyword: "" },
        records: { keyword: "" },
      },
      lists: {
        poems: emptyPage(),
        users: emptyPage(),
        topics: emptyPage(),
        comments: emptyPage(),
        feedback: emptyPage(),
        rooms: emptyPage(),
        records: emptyPage(),
      },
      dialogs: { poem: false, category: false, user: false, topic: false, room: false },
      forms: {
        poem: {},
        category: {},
        user: {},
        topic: {},
        room: {},
      },
    };
  },
  computed: {
    pageTitle() {
      const map = {
        dashboard: "运营仪表盘",
        poems: "诗词内容",
        categories: "分类管理",
        users: "用户管理",
        topics: "广场帖子",
        comments: "评论审核",
        feedback: "反馈处理",
        rooms: "飞花令房间",
        records: "答题记录",
        system: "系统设置",
      };
      return map[this.active] || "管理后台";
    },
    pageSubtitle() {
      const map = {
        dashboard: "总览内容、用户、社区与反馈状态",
        poems: "维护诗词正文、标签、推荐句与分类关联",
        categories: "管理小程序分类入口和排序",
        users: "查看用户画像并修正展示资料",
        topics: "审核和维护广场帖子内容",
        comments: "处理评论内容风险",
        feedback: "跟进用户反馈处理状态",
        rooms: "维护飞花令房间状态",
        records: "查看飞花令答题结果",
        system: "配置后台连接和检查服务健康",
      };
      return map[this.active] || "";
    },
    metrics() {
      const c = this.dashboard.counts || {};
      return [
        { key: "poems", label: "诗词", value: c.poems || 0 },
        { key: "users", label: "用户", value: c.users || 0 },
        { key: "topics", label: "帖子", value: c.topics || 0 },
        { key: "feedback", label: "反馈", value: c.feedback || 0 },
        { key: "categories", label: "分类", value: c.categories || 0 },
        { key: "comments", label: "评论", value: c.comments || 0 },
        { key: "rooms", label: "房间", value: c.rooms || 0 },
        { key: "records", label: "记录", value: c.records || 0 },
      ];
    },
  },
  created() {
    if (this.token) {
      this.bootstrap();
    }
  },
  methods: {
    headers() {
      return this.token ? { Authorization: `Bearer ${this.token}` } : {};
    },
    async request(method, path, data, params) {
      const response = await axios({
        method,
        url: `${this.apiBase}${path}`,
        data,
        params,
        headers: this.headers(),
      });
      const body = response.data || {};
      if (body.code !== 0) {
        throw new Error(body.message || "请求失败");
      }
      return body.data;
    },
    async login() {
      this.loading.login = true;
      try {
        localStorage.setItem("admin_api_base", this.apiBase);
        const data = await this.request("post", "/admin/auth/login", this.loginForm);
        this.token = data.token;
        this.currentUser = data.username;
        localStorage.setItem("admin_token", data.token);
        localStorage.setItem("admin_username", data.username);
        this.$message.success("登录成功");
        await this.bootstrap();
      } catch (error) {
        this.$message.error(this.errorText(error));
      } finally {
        this.loading.login = false;
      }
    },
    logout() {
      this.token = "";
      this.currentUser = "";
      localStorage.removeItem("admin_token");
      localStorage.removeItem("admin_username");
    },
    errorText(error) {
      const data = error.response && error.response.data;
      if (error.response && error.response.status === 404) {
        return "当前后端未加载管理接口，请重启 backend 服务后再登录";
      }
      if (data && data.message) return data.message;
      return error.message || "操作失败";
    },
    async bootstrap() {
      await this.fetchCategories();
      await this.refreshActive();
    },
    selectMenu(index) {
      this.active = index;
      localStorage.setItem("admin_active", index);
      this.refreshActive();
    },
    refreshActive() {
      const actions = {
        dashboard: this.fetchDashboard,
        poems: this.fetchPoems,
        categories: this.fetchCategories,
        users: this.fetchUsers,
        topics: this.fetchTopics,
        comments: this.fetchComments,
        feedback: this.fetchFeedback,
        rooms: this.fetchRooms,
        records: this.fetchRecords,
        system: this.checkHealth,
      };
      return actions[this.active] ? actions[this.active]() : Promise.resolve();
    },
    async fetchDashboard() {
      this.dashboard = await this.request("get", "/admin/dashboard");
    },
    async fetchCategories() {
      const data = await this.request("get", "/admin/categories");
      this.categories = data.items || [];
    },
    async fetchPoems() {
      const state = this.lists.poems;
      this.lists.poems = await this.request("get", "/admin/poems", null, {
        page: state.page,
        page_size: state.page_size,
        ...this.filters.poems,
      });
    },
    async fetchUsers() {
      const state = this.lists.users;
      this.lists.users = await this.request("get", "/admin/users", null, {
        page: state.page,
        page_size: state.page_size,
        keyword: this.filters.users.keyword,
      });
    },
    async fetchTopics() {
      const state = this.lists.topics;
      this.lists.topics = await this.request("get", "/admin/square/topics", null, {
        page: state.page,
        page_size: state.page_size,
        keyword: this.filters.topics.keyword,
        user_id: this.filters.topics.user_id || undefined,
      });
    },
    async fetchComments() {
      const state = this.lists.comments;
      this.lists.comments = await this.request("get", "/admin/square/comments", null, {
        page: state.page,
        page_size: state.page_size,
        keyword: this.filters.comments.keyword,
        topic_id: this.filters.comments.topic_id || undefined,
      });
    },
    async fetchFeedback() {
      const state = this.lists.feedback;
      this.lists.feedback = await this.request("get", "/admin/feedback", null, {
        page: state.page,
        page_size: state.page_size,
        status: this.filters.feedback.status,
      });
    },
    async fetchRooms() {
      const state = this.lists.rooms;
      this.lists.rooms = await this.request("get", "/admin/feihualing/rooms", null, {
        page: state.page,
        page_size: state.page_size,
        keyword: this.filters.rooms.keyword,
      });
    },
    async fetchRecords() {
      const state = this.lists.records;
      this.lists.records = await this.request("get", "/admin/feihualing/records", null, {
        page: state.page,
        page_size: state.page_size,
        keyword: this.filters.records.keyword,
      });
    },
    changePage(key, next) {
      this.lists[key].page = next.page;
      this.lists[key].page_size = next.page_size;
      const map = {
        poems: this.fetchPoems,
        users: this.fetchUsers,
        topics: this.fetchTopics,
        comments: this.fetchComments,
        feedback: this.fetchFeedback,
        rooms: this.fetchRooms,
        records: this.fetchRecords,
      };
      map[key]();
    },
    openPoem(row) {
      this.forms.poem = row
        ? { ...row, category_ids: [...(row.category_ids || [])], tagsText: (row.tags || []).join("，") }
        : {
            title: "",
            dynasty: "",
            author: "",
            content: "",
            recommend_sentence: "",
            category_ids: [],
            tagsText: "",
            like_count: 0,
            favorite_count: 0,
            share_count: 0,
          };
      this.dialogs.poem = true;
    },
    async savePoem() {
      const form = this.forms.poem;
      const payload = {
        title: form.title,
        dynasty: form.dynasty,
        author: form.author,
        content: form.content,
        recommend_sentence: form.recommend_sentence || "",
        tags: splitList(form.tagsText),
        category_ids: form.category_ids || [],
        like_count: form.like_count || 0,
        favorite_count: form.favorite_count || 0,
        share_count: form.share_count || 0,
      };
      if (form.id) await this.request("put", `/admin/poems/${form.id}`, payload);
      else await this.request("post", "/admin/poems", payload);
      this.dialogs.poem = false;
      this.$message.success("诗词已保存");
      await this.fetchPoems();
      await this.fetchCategories();
    },
    openCategory(row) {
      this.forms.category = row ? { ...row } : { name: "", type: "theme", sort_order: 0 };
      this.dialogs.category = true;
    },
    async saveCategory() {
      const form = this.forms.category;
      const payload = { name: form.name, type: form.type, sort_order: form.sort_order || 0 };
      if (form.id) await this.request("put", `/admin/categories/${form.id}`, payload);
      else await this.request("post", "/admin/categories", payload);
      this.dialogs.category = false;
      this.$message.success("分类已保存");
      await this.fetchCategories();
    },
    openUser(row) {
      this.forms.user = { ...row };
      this.dialogs.user = true;
    },
    async saveUser() {
      const form = this.forms.user;
      await this.request("put", `/admin/users/${form.id}`, {
        nickname: form.nickname,
        avatar_text: form.avatar_text,
        title: form.title,
        level: form.level,
        gender: form.gender,
        city: form.city,
        bio: form.bio,
      });
      this.dialogs.user = false;
      this.$message.success("用户资料已保存");
      await this.fetchUsers();
    },
    openTopic(row) {
      this.forms.topic = {
        ...row,
        tagsText: (row.tags || []).join("，"),
        imagesText: (row.images || []).join("，"),
      };
      this.dialogs.topic = true;
    },
    async saveTopic() {
      const form = this.forms.topic;
      await this.request("put", `/admin/square/topics/${form.id}`, {
        title: form.title,
        content: form.content,
        badge: form.badge,
        tags: splitList(form.tagsText),
        images: splitList(form.imagesText),
      });
      this.dialogs.topic = false;
      this.$message.success("帖子已保存");
      await this.fetchTopics();
    },
    openRoom(row) {
      this.forms.room = { ...row };
      this.dialogs.room = true;
    },
    async saveRoom() {
      const form = this.forms.room;
      await this.request("put", `/admin/feihualing/rooms/${form.id}`, {
        title: form.title,
        keyword: form.keyword,
        can_watch: form.can_watch,
        player_count: form.player_count,
        max_players: form.max_players,
        round_text: form.round_text,
      });
      this.dialogs.room = false;
      this.$message.success("房间已保存");
      await this.fetchRooms();
    },
    async updateFeedback(id, status) {
      await this.request("put", `/admin/feedback/${id}`, { status });
      this.$message.success("反馈状态已更新");
      await this.fetchFeedback();
    },
    async removeItem(type, id) {
      const config = {
        poems: ["/admin/poems", this.fetchPoems],
        categories: ["/admin/categories", this.fetchCategories],
        topics: ["/admin/square/topics", this.fetchTopics],
        comments: ["/admin/square/comments", this.fetchComments],
        feedback: ["/admin/feedback", this.fetchFeedback],
        rooms: ["/admin/feihualing/rooms", this.fetchRooms],
      }[type];
      if (!config) return;
      await this.$confirm("删除后不可恢复，确认继续？", "确认删除", { type: "warning" });
      await this.request("delete", `${config[0]}/${id}`);
      this.$message.success("已删除");
      await config[1]();
    },
    trendWidth(item) {
      const total = (item.users || 0) + (item.topics || 0) + (item.feedback || 0);
      const max = Math.max(
        1,
        ...this.dashboard.trend.map((row) => (row.users || 0) + (row.topics || 0) + (row.feedback || 0))
      );
      return Math.max(4, Math.round((total / max) * 100));
    },
    saveApiBase() {
      localStorage.setItem("admin_api_base", this.apiBase);
      this.$message.success("接口地址已保存");
    },
    async checkHealth() {
      try {
        await this.request("get", "/admin/system/health");
        this.$message.success("后台 API 连接正常");
      } catch (error) {
        this.$message.error(this.errorText(error));
      }
    },
  },
});
