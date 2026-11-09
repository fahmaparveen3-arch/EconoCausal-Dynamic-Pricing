"use client";

import { useEffect, useState } from "react";
import {
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  Bell,
  Brain,
  CheckCircle2,
  ChevronDown,
  CircleHelp,
  Download,
  LayoutDashboard,
  Menu,
  Moon,
  Search,
  ShieldAlert,
  ShoppingCart,
  Sun,
  Target,
  TrendingUp,
  Users,
  X,
  Zap,
} from "lucide-react";

import {
  Area,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { AnimatePresence, motion } from "motion/react";

type Section =
  | "Overview"
  | "Pricing Analytics"
  | "Causal Analysis"
  | "Uplift Analysis"
  | "Model Insights";

const navigation = [
  { name: "Overview" as Section, icon: LayoutDashboard },
  { name: "Pricing Analytics" as Section, icon: ShoppingCart },
  { name: "Causal Analysis" as Section, icon: Activity },
  { name: "Uplift Analysis" as Section, icon: Target },
  { name: "Model Insights" as Section, icon: Brain },
];

const segmentColors = ["#10b981", "#3b82f6", "#64748b"];

const tooltipStyle = {
  backgroundColor: "#111827",
  border: "1px solid #334155",
  borderRadius: "10px",
  color: "#f8fafc",
};

function MetricCard({
  title,
  value,
  change,
  icon: Icon,
  positive = true,
  description,
}: {
  title: string;
  value: string;
  change?: string;
  icon: React.ElementType;
  positive?: boolean;
  description?: string;
}) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      className="rounded-2xl border border-slate-700/60 bg-slate-900/80 p-5 shadow-lg shadow-black/10"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{title}</p>
        <div className="rounded-xl bg-emerald-500/10 p-2">
          <Icon size={19} className="text-emerald-400" />
        </div>
      </div>

      <div className="mt-5 flex items-end justify-between gap-2">
        <h3 className="text-2xl font-semibold tracking-tight text-white">
          {value}
        </h3>

        {change && (
          <span
            className={`flex items-center gap-1 text-xs ${
              positive ? "text-emerald-400" : "text-rose-400"
            }`}
          >
            {positive ? (
              <ArrowUpRight size={14} />
            ) : (
              <ArrowDownRight size={14} />
            )}
            {change}
          </span>
        )}
      </div>

      {description && (
        <p className="mt-2 text-xs text-slate-500">{description}</p>
      )}
    </motion.div>
  );
}

function ChartCard({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-slate-700/60 bg-slate-900/80 p-5 shadow-lg shadow-black/10">
      <div className="mb-5">
        <h3 className="font-semibold text-white">{title}</h3>
        <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
      </div>
      {children}
    </div>
  );
}

function SectionHeading({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="mb-7">
      <h2 className="text-2xl font-semibold tracking-tight text-white">
        {title}
      </h2>
      <p className="mt-2 text-sm text-slate-400">{subtitle}</p>
    </div>
  );
}

export default function Home() {
  const [activeSection, setActiveSection] = useState<Section>("Overview");
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [themeReady, setThemeReady] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [apiData, setApiData] = useState<{
    overview: any;
    pricing: any;
    causal: any;
    uplift: any;
    modelInsights: any;
  } | null>(null);
  const [apiLoading, setApiLoading] = useState(true);
  const [apiError, setApiError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function loadDashboardData() {
      try {
        setApiLoading(true);
        setApiError("");

        const endpoints = [
          "overview",
          "pricing",
          "causal",
          "uplift",
          "model-insights",
        ];

        const responses = await Promise.all(
          endpoints.map((endpoint) =>
            fetch(`http://127.0.0.1:8000/api/${endpoint}`, {
              signal: controller.signal,
            })
          )
        );

        const failedResponse = responses.find((response) => !response.ok);
        if (failedResponse) {
          throw new Error(`Backend request failed: ${failedResponse.status}`);
        }

        const [overview, pricing, causal, uplift, modelInsights] =
          await Promise.all(responses.map((response) => response.json()));

        if (!controller.signal.aborted) {
          setApiData({ overview, pricing, causal, uplift, modelInsights });
        }
      } catch (error) {
        if (!controller.signal.aborted) {
          setApiError(
            error instanceof Error ? error.message : "Unable to load dashboard data."
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setApiLoading(false);
        }
      }
    }

    loadDashboardData();

    return () => controller.abort();
  }, []);

  useEffect(() => {
    const savedTheme = window.localStorage.getItem("econocausal-theme");

    const frameId = window.requestAnimationFrame(() => {
      if (savedTheme === "light" || savedTheme === "dark") {
        setTheme(savedTheme);
      }
      setThemeReady(true);
    });

    return () => window.cancelAnimationFrame(frameId);
  }, []);

  useEffect(() => {
    if (themeReady) {
      window.localStorage.setItem("econocausal-theme", theme);
    }
  }, [theme, themeReady]);

  const isDark = theme === "dark";
  const pricingData = apiData?.pricing?.policies?.map((item: any) => ({
    discount: item.discount,
    profit: item.profit,
    revenue: item.revenue,
  })) ?? [];

  const treatmentData = apiData?.causal?.effects ?? [];
  const segmentData = apiData?.causal?.segment_counts ?? [];

  const searchableData: { section: Section; data: any }[] = apiData
    ? [
        { section: "Overview", data: apiData.overview },
        { section: "Pricing Analytics", data: apiData.pricing },
        { section: "Causal Analysis", data: apiData.causal },
        { section: "Uplift Analysis", data: apiData.uplift },
        { section: "Model Insights", data: apiData.modelInsights },
      ]
    : [];

  const searchIndex = searchableData.flatMap(({ section, data }) => {
    const items: { section: Section; label: string; value: string }[] = [];

    const collect = (value: any, label: string) => {
      if (Array.isArray(value)) {
        value.forEach((item, index) => collect(item, `${label} ${index + 1}`));
      } else if (value !== null && typeof value === "object") {
        Object.entries(value).forEach(([key, nested]) =>
          collect(nested, `${label} ${key.replace(/_/g, " ")}`)
        );
      } else if (value !== null && value !== undefined) {
        items.push({ section, label, value: String(value) });
      }
    };

    collect(data, section);
    return items;
  });

  const searchResults = searchQuery.trim()
    ? searchIndex
        .filter((item) =>
          `${item.section} ${item.label} ${item.value}`
            .toLowerCase()
            .includes(searchQuery.trim().toLowerCase())
        )
        .slice(0, 10)
    : [];

  const modelMetrics = apiData
    ? [
        {
          label: "Qini coefficient",
          value: String(apiData.uplift.metrics.qini_coefficient),
          description: "Uplift model ranking metric",
        },
        {
          label: "Predicted uplift",
          value: `+${apiData.uplift.metrics.predicted_mean_uplift} pp`,
          description: "T-learner estimated uplift",
        },
        {
          label: "Top 20% uplift",
          value: `+${apiData.uplift.metrics.top_20_percent_uplift} pp`,
          description: "Observed uplift in top segment",
        },
        {
          label: "DML holdout ATE",
          value: apiData.modelInsights.primary_validation.estimated_ate.toFixed(4),
          description: "Synthetic validation estimate",
        },
      ]
    : [];


  const pageBackground = isDark
    ? "bg-[#080f1c] text-white"
    : "bg-slate-100 text-slate-900";

  const sidebarBackground = isDark
    ? "bg-[#0c1524] border-slate-800"
    : "bg-white border-slate-200";

  const headerBackground = isDark
    ? "bg-[#0c1524]/90 border-slate-800"
    : "bg-white/90 border-slate-200";

  const cardBackground = isDark
    ? "bg-slate-900/80 border-slate-700/60"
    : "bg-white border-slate-200";

  const primaryText = isDark ? "text-white" : "text-slate-900";
  const secondaryText = isDark ? "text-slate-400" : "text-slate-500";

  function toggleTheme() {
    setTheme((current) => (current === "dark" ? "light" : "dark"));
  }

  function changeSection(section: Section) {
    setActiveSection(section);
    setMobileMenuOpen(false);
  }

  function exportReport() {
    const report = [
      "EconoCausal - Dynamic Pricing Analytics Report",
      "",
      "Pricing analysis (synthetic dataset)",
      ...pricingData.map(
        (item: any) =>
          `Discount: ${item.discount}, Expected profit/customer: $${item.profit}`
      ),
      "",
      "Hillstrom treatment effects",
      ...treatmentData.map(
        (item: any) =>
          `${item.segment}: +${item.effect} percentage points`
      ),
      "",
      "Model metrics",
      ...modelMetrics.map(
        (item) => `${item.label}: ${item.value}`
      ),
      "",
      "Note: Pricing results are based on synthetic data. Observational results do not establish causality.",
    ].join("\n");

    const blob = new Blob([report], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "econocausal-report.txt";
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className={`min-h-screen ${pageBackground}`}>
      <div className="flex min-h-screen">
        {/* Desktop sidebar */}
        <aside
          className={`fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r lg:flex ${sidebarBackground}`}
        >
          <div className="flex h-20 items-center gap-3 border-b border-slate-800 px-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500">
              <Activity className="text-white" size={23} />
            </div>
            <div>
              <h1 className={`text-lg font-bold ${primaryText}`}>
                EconoCausal
              </h1>
              <p className="text-xs text-slate-500">Intelligence Platform</p>
            </div>
          </div>

          <div className="px-5 pt-8">
            <p className="mb-4 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-500">
              Workspace
            </p>

            <nav className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                const active = activeSection === item.name;

                return (
                  <button
                    key={item.name}
                    onClick={() => changeSection(item.name)}
                    className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm transition-all ${
                      active
                        ? "bg-emerald-500/15 font-medium text-emerald-400"
                        : `${secondaryText} hover:bg-slate-800/60 hover:text-white`
                    }`}
                  >
                    <Icon size={19} />
                    {item.name}
                    {active && (
                      <span className="ml-auto h-2 w-2 rounded-full bg-emerald-400" />
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          <div className="mt-auto p-5">
            <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-4">
              <div className="flex items-center gap-2 text-emerald-400">
                <Zap size={16} />
                <span className="text-xs font-semibold">Decision Support</span>
              </div>
              <p className="mt-2 text-xs leading-5 text-slate-400">
                Data-driven insights for pricing and marketing decisions.
              </p>
            </div>

            <div className="mt-5 flex items-center gap-3 px-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-700 text-sm font-semibold text-white">
                EC
              </div>
              <div>
                <p className={`text-sm font-medium ${primaryText}`}>
                  Project Workspace
                </p>
                <p className="text-xs text-slate-500">Analytics dashboard</p>
              </div>
            </div>
          </div>
        </aside>

        {/* Mobile sidebar */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-40 bg-black/60 lg:hidden"
                onClick={() => setMobileMenuOpen(false)}
              />

              <motion.aside
                initial={{ x: -280 }}
                animate={{ x: 0 }}
                exit={{ x: -280 }}
                transition={{ duration: 0.25 }}
                className={`fixed inset-y-0 left-0 z-50 w-72 border-r p-5 lg:hidden ${sidebarBackground}`}
              >
                <div className="mb-8 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Activity className="text-emerald-400" />
                    <span className={`font-bold ${primaryText}`}>
                      EconoCausal
                    </span>
                  </div>
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="rounded-lg p-2 hover:bg-slate-700/30"
                    aria-label="Close menu"
                  >
                    <X size={20} />
                  </button>
                </div>

                <nav className="space-y-2">
                  {navigation.map((item) => {
                    const Icon = item.icon;
                    return (
                      <button
                        key={item.name}
                        onClick={() => changeSection(item.name)}
                        className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm ${
                          activeSection === item.name
                            ? "bg-emerald-500/15 text-emerald-400"
                            : `${secondaryText} hover:bg-slate-700/30`
                        }`}
                      >
                        <Icon size={19} />
                        {item.name}
                      </button>
                    );
                  })}
                </nav>
              </motion.aside>
            </>
          )}
        </AnimatePresence>

        {/* Main content */}
        <main className="min-w-0 flex-1 lg:ml-64">
          {/* Top header */}
          <header
            className={`sticky top-0 z-30 flex h-20 items-center justify-between border-b px-4 backdrop-blur-xl sm:px-7 lg:px-10 ${headerBackground}`}
          >
            <div className="flex items-center gap-3">
              <button
                className="rounded-lg p-2 hover:bg-slate-700/20 lg:hidden"
                onClick={() => setMobileMenuOpen(true)}
                aria-label="Open menu"
              >
                <Menu size={21} />
              </button>

              <div>
                <p className={`text-sm font-semibold ${primaryText}`}>
                  {activeSection}
                </p>
                <p className="text-xs text-slate-500">
                  EconoCausal / {activeSection}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 sm:gap-4">
              <div className="relative hidden md:block">
                <div
                  className={`flex w-64 items-center gap-2 rounded-xl border px-3 py-2 ${
                    isDark
                      ? "border-slate-700 bg-slate-900"
                      : "border-slate-200 bg-slate-50"
                  }`}
                >
                  <Search size={15} className="shrink-0 text-slate-500" />
                  <input
                    type="search"
                    value={searchQuery}
                    onChange={(event) => {
                      setSearchQuery(event.target.value);
                      setSearchOpen(true);
                    }}
                    onFocus={() => setSearchOpen(true)}
                    onKeyDown={(event) => {
                      if (event.key === "Escape") {
                        setSearchOpen(false);
                        event.currentTarget.blur();
                      }
                    }}
                    placeholder="Search dashboard..."
                    aria-label="Search all dashboard content"
                    className={`w-full bg-transparent text-xs outline-none ${
                      isDark
                        ? "text-white placeholder:text-slate-500"
                        : "text-slate-900 placeholder:text-slate-400"
                    }`}
                  />
                  {searchQuery && (
                    <button
                      type="button"
                      onClick={() => {
                        setSearchQuery("");
                        setSearchOpen(false);
                      }}
                      aria-label="Clear search"
                      className="text-slate-500 hover:text-slate-300"
                    >
                      <X size={14} />
                    </button>
                  )}
                </div>

                {searchOpen && searchQuery.trim() && (
                  <div
                    className={`absolute right-0 top-full z-50 mt-2 max-h-80 w-80 overflow-y-auto rounded-xl border p-2 shadow-xl ${
                      isDark
                        ? "border-slate-700 bg-slate-900"
                        : "border-slate-200 bg-white"
                    }`}
                  >
                    {apiLoading ? (
                      <p className="p-3 text-xs text-slate-500">
                        Loading dashboard data...
                      </p>
                    ) : searchResults.length > 0 ? (
                      searchResults.map((result, index) => (
                        <button
                          type="button"
                          key={`${result.section}-${result.label}-${index}`}
                          onClick={() => {
                            changeSection(result.section);
                            setSearchOpen(false);
                          }}
                          className={`block w-full rounded-lg px-3 py-2 text-left transition ${
                            isDark
                              ? "hover:bg-slate-800"
                              : "hover:bg-slate-100"
                          }`}
                        >
                          <span className="block text-xs font-semibold text-emerald-500">
                            {result.section}
                          </span>
                          <span
                            className={`mt-1 block break-words text-xs ${
                              isDark ? "text-slate-300" : "text-slate-600"
                            }`}
                          >
                            {result.label}: {result.value}
                          </span>
                        </button>
                      ))
                    ) : (
                      <p className="p-3 text-xs text-slate-500">
                        No matching dashboard content found.
                      </p>
                    )}
                  </div>
                )}
              </div>

              <button
                onClick={toggleTheme}
                aria-label="Toggle theme"
                className={`rounded-xl border p-2.5 transition hover:scale-105 ${
                  isDark
                    ? "border-slate-700 bg-slate-900 text-amber-300"
                    : "border-slate-200 bg-white text-slate-700"
                }`}
              >
                {isDark ? <Sun size={18} /> : <Moon size={18} />}
              </button>

              <button
                aria-label="Notifications"
                className={`relative rounded-xl border p-2.5 ${
                  isDark
                    ? "border-slate-700 bg-slate-900 text-slate-300"
                    : "border-slate-200 bg-white text-slate-600"
                }`}
              >
                <Bell size={18} />
                <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-emerald-400" />
              </button>

              <div className="hidden items-center gap-2 sm:flex">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-500/15 text-xs font-bold text-emerald-400">
                  EC
                </div>
                <ChevronDown size={15} className="text-slate-500" />
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-[1600px] p-4 sm:p-7 lg:p-10">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeSection}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.22 }}
              >
                {/* OVERVIEW */}
                {activeSection === "Overview" && (
                  <div>
                    <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
                      <div>
                        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-emerald-400">
                          Analytics overview
                        </p>
                        <h2 className="text-3xl font-bold tracking-tight">
                          Welcome to EconoCausal
                        </h2>
                        <p className={`mt-2 text-sm ${secondaryText}`}>
                          Explore pricing performance, causal effects and
                          predictive insights.
                        </p>
                      </div>

                      <button
                        onClick={exportReport}
                        className="flex items-center justify-center gap-2 rounded-xl bg-emerald-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-400"
                      >
                        <Download size={17} />
                        Export report
                      </button>
                    </div>

                    <div className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                      <MetricCard
                        title="Customers analysed"
                        value={apiData?.overview?.customers_analysed?.toLocaleString() ?? "Loading..."}
                        change="Hillstrom dataset"
                        icon={Users}
                        description="Randomized marketing experiment"
                      />
                      <MetricCard
                        title="Best synthetic discount"
                        value={apiData?.overview?.best_discount ?? "Loading..."}
                        change="Highest expected profit"
                        icon={TrendingUp}
                        description={apiData?.overview?.expected_profit_per_customer != null ? `$${apiData.overview.expected_profit_per_customer.toFixed(2)} expected profit/customer` : "Loading pricing result"}
                      />
                      <MetricCard
                        title="Uplift model Qini"
                        value={apiData?.overview?.qini_coefficient?.toFixed(4) ?? "Loading..."}
                        change="Model metric"
                        icon={Target}
                        description="T-learner uplift evaluation"
                      />
                      <MetricCard
                        title="Treatment effect"
                        value={apiData?.causal?.effects?.find((item: any) => item.segment === "Men's Email") ? `+${apiData.causal.effects.find((item: any) => item.segment === "Men's Email").effect.toFixed(3)} pp` : "Loading..."}
                        change="Men's Email"
                        icon={Activity}
                        description="Compared with No Email"
                      />
                    </div>

                    <div className="grid gap-5 xl:grid-cols-2">
                      <ChartCard
                        title="Discount vs expected profit"
                        subtitle="Synthetic pricing experiment · Profit per customer"
                      >
                        <div className="h-72">
                          <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart data={pricingData}>
                              <defs>
                                <linearGradient
                                  id="profitGradient"
                                  x1="0"
                                  y1="0"
                                  x2="0"
                                  y2="1"
                                >
                                  <stop
                                    offset="0%"
                                    stopColor="#10b981"
                                    stopOpacity={0.3}
                                  />
                                  <stop
                                    offset="100%"
                                    stopColor="#10b981"
                                    stopOpacity={0}
                                  />
                                </linearGradient>
                              </defs>
                              <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="#334155"
                                vertical={false}
                              />
                              <XAxis
                                dataKey="discount"
                                stroke="#94a3b8"
                                tickLine={false}
                                axisLine={false}
                              />
                              <YAxis
                                stroke="#94a3b8"
                                tickLine={false}
                                axisLine={false}
                              />
                              <Tooltip contentStyle={tooltipStyle} />
                              <Area
                                type="monotone"
                                dataKey="profit"
                                fill="url(#profitGradient)"
                                stroke="#10b981"
                                strokeWidth={2.5}
                              />
                              <Line
                                type="monotone"
                                dataKey="revenue"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                dot={{ r: 3 }}
                              />
                              <Legend />
                            </ComposedChart>
                          </ResponsiveContainer>
                        </div>
                      </ChartCard>

                      <ChartCard
                        title="Customer segment distribution"
                        subtitle="Hillstrom randomized marketing dataset"
                      >
                        <div className="flex h-72 flex-col items-center justify-center sm:flex-row">
                          <div className="h-60 w-full sm:w-1/2">
                            <ResponsiveContainer width="100%" height="100%">
                              <PieChart>
                                <Pie
                                  data={segmentData}
                                  dataKey="value"
                                  nameKey="name"
                                  cx="50%"
                                  cy="50%"
                                  innerRadius={55}
                                  outerRadius={90}
                                  paddingAngle={4}
                                >
                                  {segmentData.map((entry: any, index: number) => (
                                    <Cell
                                      key={entry.name}
                                      fill={segmentColors[index]}
                                    />
                                  ))}
                                </Pie>
                                <Tooltip contentStyle={tooltipStyle} />
                              </PieChart>
                            </ResponsiveContainer>
                          </div>

                          <div className="space-y-5">
                            {segmentData.map((segment: any, index: number) => (
                              <div key={segment.name}>
                                <div className="flex items-center gap-2">
                                  <span
                                    className="h-2.5 w-2.5 rounded-full"
                                    style={{
                                      backgroundColor: segmentColors[index],
                                    }}
                                  />
                                  <span className="text-xs text-slate-400">
                                    {segment.name}
                                  </span>
                                </div>
                                <p className="ml-5 mt-1 text-lg font-semibold text-white">
                                  {segment.value.toLocaleString()}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      </ChartCard>

                      <ChartCard
                        title="Estimated treatment effects"
                        subtitle="Email campaigns compared with No Email · Percentage points"
                      >
                        <div className="h-72">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                              data={treatmentData}
                              layout="vertical"
                              margin={{ left: 15, right: 25 }}
                            >
                              <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="#334155"
                                horizontal={false}
                              />
                              <XAxis
                                type="number"
                                stroke="#94a3b8"
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(value) => `${value} pp`}
                              />
                              <YAxis
                                type="category"
                                dataKey="segment"
                                stroke="#94a3b8"
                                tickLine={false}
                                axisLine={false}
                                width={100}
                              />
                              <Tooltip
                                contentStyle={tooltipStyle}
                                formatter={(value) => [
                                  `${Number(value).toFixed(3)} pp`,
                                  "Estimated effect",
                                ]}
                              />
                              <Bar
                                dataKey="effect"
                                fill="#10b981"
                                radius={[0, 7, 7, 0]}
                                barSize={28}
                              />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </ChartCard>

                      <ChartCard
                        title="Model performance snapshot"
                        subtitle="Selected evaluation metrics"
                      >
                        <div className="grid gap-3 sm:grid-cols-2">
                          {modelMetrics.map((metric) => (
                            <div
                              key={metric.label}
                              className="rounded-xl border border-slate-700/60 bg-slate-800/40 p-4"
                            >
                              <p className="text-xs text-slate-400">
                                {metric.label}
                              </p>
                              <p className="mt-3 text-2xl font-semibold text-emerald-400">
                                {metric.value}
                              </p>
                              <p className="mt-2 text-xs text-slate-500">
                                {metric.description}
                              </p>
                            </div>
                          ))}
                        </div>
                      </ChartCard>
                    </div>
                  </div>
                )}

                {/* PRICING ANALYTICS */}
                {activeSection === "Pricing Analytics" && (
                  <div>
                    <SectionHeading
                      title="Pricing Analytics"
                      subtitle="Compare discount strategies using the synthetic pricing experiment."
                    />

                    <div className="mb-6 grid gap-4 sm:grid-cols-3">
                      <MetricCard
                        title="Best tested discount"
                        value={apiData?.pricing?.best_policy?.discount ?? "Loading..."}
                        icon={TrendingUp}
                        description="Highest expected profit in this experiment"
                      />
                      <MetricCard
                        title="Expected profit"
                        value={apiData?.pricing?.best_policy?.profit != null ? `$${apiData.pricing.best_policy.profit.toFixed(2)}` : "Loading..."}
                        icon={ShoppingCart}
                        description={apiData?.pricing?.best_policy?.discount ? `Per customer at ${apiData.pricing.best_policy.discount} discount` : "Loading pricing result"}
                      />
                      <MetricCard
                        title="Dataset size"
                        value={apiData?.pricing?.customers?.toLocaleString() ?? "Loading..."}
                        icon={Users}
                        description="Synthetic pricing records"
                      />
                    </div>

                    <ChartCard
                      title="Expected profit by discount"
                      subtitle="Profit per customer under each tested discount strategy"
                    >
                      <div className="h-96">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={pricingData}>
                            <CartesianGrid
                              strokeDasharray="3 3"
                              stroke="#334155"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="discount"
                              stroke="#94a3b8"
                              tickLine={false}
                              axisLine={false}
                            />
                            <YAxis
                              stroke="#94a3b8"
                              tickLine={false}
                              axisLine={false}
                            />
                            <Tooltip contentStyle={tooltipStyle} />
                            <Bar
                              dataKey="profit"
                              name="Expected profit"
                              radius={[8, 8, 0, 0]}
                              barSize={48}
                            >
                              {pricingData.map((entry: any, index: number) => (
                                <Cell
                                  key={entry.discount}
                                  fill={index === 1 ? "#10b981" : "#3b82f6"}
                                />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </ChartCard>

                    <div
                      className={`mt-6 overflow-hidden rounded-2xl border ${cardBackground}`}
                    >
                      <div className="border-b border-slate-700/50 p-5">
                        <h3 className={`font-semibold ${primaryText}`}>
                          Pricing strategy comparison
                        </h3>
                        <p className={`mt-1 text-xs ${secondaryText}`}>
                          Results from the synthetic experiment
                        </p>
                      </div>

                      <div className="overflow-x-auto">
                        <table className="w-full min-w-[500px] text-left text-sm">
                          <thead className="bg-slate-800/40 text-xs text-slate-400">
                            <tr>
                              <th className="px-5 py-4">Discount</th>
                              <th className="px-5 py-4">Expected profit</th>
                              <th className="px-5 py-4">Revenue</th>
                              <th className="px-5 py-4">Result</th>
                            </tr>
                          </thead>
                          <tbody>
                            {pricingData.map((item: any, index: number) => (
                              <tr
                                key={item.discount}
                                className="border-t border-slate-700/40"
                              >
                                <td className={`px-5 py-4 ${primaryText}`}>
                                  {item.discount}
                                </td>
                                <td className="px-5 py-4 font-semibold text-emerald-400">
                                  ${item.profit.toFixed(2)}
                                </td>
                                <td className={`px-5 py-4 ${secondaryText}`}>
                                  ${item.revenue.toFixed(2)}
                                </td>
                                <td className="px-5 py-4">
                                  {index === 1 ? (
                                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                                      Best tested
                                    </span>
                                  ) : (
                                    <span className="text-xs text-slate-500">
                                      Compared
                                    </span>
                                  )}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <p className="mt-4 text-xs text-slate-500">
                      Note: These results are based on synthetic data and
                      assumptions. The 5% discount is not a proven real-world
                      optimal pricing strategy.
                    </p>
                  </div>
                )}

                {/* CAUSAL ANALYSIS */}
                {activeSection === "Causal Analysis" && (
                  <div>
                    <SectionHeading
                      title="Causal Analysis"
                      subtitle="Understand the estimated effect of email marketing interventions."
                    />

                    <div className="mb-6 grid gap-4 sm:grid-cols-2">
                      <MetricCard
                        title="Men's Email effect"
                        value={treatmentData.find((item: any) => item.segment === "Men's Email") ? `+${treatmentData.find((item: any) => item.segment === "Men's Email").effect.toFixed(3)} pp` : "Loading..."}
                        icon={ArrowUpRight}
                        description="Compared with No Email"
                      />
                      <MetricCard
                        title="Women's Email effect"
                        value={treatmentData.find((item: any) => item.segment === "Women's Email") ? `+${treatmentData.find((item: any) => item.segment === "Women's Email").effect.toFixed(3)} pp` : "Loading..."}
                        icon={ArrowUpRight}
                        description="Compared with No Email"
                      />
                    </div>

                    <ChartCard
                      title="Estimated average treatment effects"
                      subtitle="Conversion rate difference in percentage points"
                    >
                      <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={treatmentData}
                            layout="vertical"
                            margin={{ left: 15, right: 25 }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              stroke="#334155"
                              horizontal={false}
                            />
                            <XAxis
                              type="number"
                              stroke="#94a3b8"
                              tickFormatter={(value) => `${value} pp`}
                            />
                            <YAxis
                              type="category"
                              dataKey="segment"
                              stroke="#94a3b8"
                              width={110}
                            />
                            <Tooltip
                              contentStyle={tooltipStyle}
                              formatter={(value) => [
                                `${Number(value).toFixed(3)} pp`,
                                "Treatment effect",
                              ]}
                            />
                            <Bar
                              dataKey="effect"
                              fill="#10b981"
                              radius={[0, 7, 7, 0]}
                              barSize={35}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </ChartCard>

                    <div className="mt-6 grid gap-5 lg:grid-cols-2">
                      <div className={`rounded-2xl border p-5 ${cardBackground}`}>
                        <div className="mb-4 flex items-center gap-2">
                          <CheckCircle2 className="text-emerald-400" size={20} />
                          <h3 className={`font-semibold ${primaryText}`}>
                            Men&apos;s Email
                          </h3>
                        </div>
                        <p className="text-3xl font-bold text-emerald-400">
                          {treatmentData.find((item: any) => item.segment === "Men's Email") ? `+${treatmentData.find((item: any) => item.segment === "Men's Email").effect.toFixed(3)} pp` : "Loading..."}
                        </p>
                        <p className={`mt-3 text-sm ${secondaryText}`}>
                          95% confidence interval: [{treatmentData.find((item: any) => item.segment === "Men's Email")?.lower.toFixed(3) ?? "?"}, {treatmentData.find((item: any) => item.segment === "Men's Email")?.upper.toFixed(3) ?? "?"}]
                        </p>
                        <p className="mt-2 text-xs text-emerald-400">
                          Statistically significant
                        </p>
                      </div>

                      <div className={`rounded-2xl border p-5 ${cardBackground}`}>
                        <div className="mb-4 flex items-center gap-2">
                          <CheckCircle2 className="text-emerald-400" size={20} />
                          <h3 className={`font-semibold ${primaryText}`}>
                            Women&apos;s Email
                          </h3>
                        </div>
                        <p className="text-3xl font-bold text-emerald-400">
                          {treatmentData.find((item: any) => item.segment === "Women's Email") ? `+${treatmentData.find((item: any) => item.segment === "Women's Email").effect.toFixed(3)} pp` : "Loading..."}
                        </p>
                        <p className={`mt-3 text-sm ${secondaryText}`}>
                          95% confidence interval: [{treatmentData.find((item: any) => item.segment === "Women's Email")?.lower.toFixed(3) ?? "?"}, {treatmentData.find((item: any) => item.segment === "Women's Email")?.upper.toFixed(3) ?? "?"}]
                        </p>
                        <p className="mt-2 text-xs text-emerald-400">
                          Statistically significant | p = {treatmentData.find((item: any) => item.segment === "Women's Email")?.p_value?.toExponential(2) ?? "?"}
                        </p>
                      </div>
                    </div>

                    <div className="mt-6 rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">
                      <h3 className="font-semibold text-blue-400">
                        What does this mean?
                      </h3>
                      <p className="mt-2 text-sm leading-6 text-slate-400">
                        The Hillstrom experiment compares email marketing
                        groups with a no-email control group. The estimated
                        effects show how much the conversion rate changed
                        relative to the control group. These are experimental
                        estimates, not guaranteed outcomes for every business.
                      </p>
                    </div>
                  </div>
                )}

                {/* UPLIFT ANALYSIS */}
                {activeSection === "Uplift Analysis" && (
                  <div>
                    <SectionHeading
                      title="Uplift Analysis"
                      subtitle="Estimate which customers may respond differently to a marketing intervention."
                    />

                    <div className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                      <MetricCard
                        title="Qini coefficient"
                        value={apiData?.uplift?.metrics?.qini_coefficient?.toFixed(4) ?? "Loading..."}
                        icon={Target}
                        description="Uplift model ranking metric"
                      />
                      <MetricCard
                        title="Predicted uplift"
                        value={apiData?.uplift?.metrics?.predicted_mean_uplift != null ? `+${apiData.uplift.metrics.predicted_mean_uplift.toFixed(3)} pp` : "Loading..."}
                        icon={TrendingUp}
                        description="T-learner estimated uplift"
                      />
                      <MetricCard
                        title="Top 20% uplift"
                        value={apiData?.uplift?.metrics?.top_20_percent_uplift != null ? `+${apiData.uplift.metrics.top_20_percent_uplift.toFixed(3)} pp` : "Loading..."}
                        icon={Users}
                        description="Observed uplift in top-ranked group"
                      />
                    </div>

                    <ChartCard
                      title="Uplift model evaluation"
                      subtitle="Predicted treatment effect by evaluation metric"
                    >
                      <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={[
                              { metric: "Predicted uplift", value: apiData?.uplift?.metrics?.predicted_mean_uplift ?? 0 },
                              { metric: "Observed test ATE", value: apiData?.uplift?.metrics?.observed_test_ate ?? 0 },
                              { metric: "Top 20% uplift", value: apiData?.uplift?.metrics?.top_20_percent_uplift ?? 0 },
                            ]}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              stroke="#334155"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="metric"
                              stroke="#94a3b8"
                              tickLine={false}
                              axisLine={false}
                            />
                            <YAxis
                              stroke="#94a3b8"
                              tickFormatter={(value) => `${value} pp`}
                            />
                            <Tooltip
                              contentStyle={tooltipStyle}
                              formatter={(value) => [
                                `${Number(value).toFixed(3)} pp`,
                                "Uplift",
                              ]}
                            />
                            <Bar
                              dataKey="value"
                              fill="#3b82f6"
                              radius={[7, 7, 0, 0]}
                              barSize={55}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </ChartCard>

                    <div className="mt-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">
                      <h3 className="font-semibold text-emerald-400">
                        How uplift modelling helps
                      </h3>
                      <p className="mt-2 text-sm leading-6 text-slate-400">
                        Traditional prediction estimates which customers are
                        likely to convert. Uplift modelling instead estimates
                        the additional impact of a treatment, such as receiving
                        a marketing email. This can help prioritize customers
                        who may benefit more from an intervention.
                      </p>
                    </div>
                  </div>
                )}

                {/* MODEL INSIGHTS */}
                {activeSection === "Model Insights" && (
                  <div>
                    <SectionHeading
                      title="Model Insights"
                      subtitle="Review model validation results, limitations and interpretation."
                    />

                    <div className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                      {modelMetrics.map((metric) => (
                        <MetricCard
                          key={metric.label}
                          title={metric.label}
                          value={metric.value}
                          icon={Brain}
                          description={metric.description}
                        />
                      ))}
                    </div>

                    <div className="grid gap-5 lg:grid-cols-2">
                      <div className={`rounded-2xl border p-5 ${cardBackground}`}>
                        <div className="mb-5 flex items-center gap-3">
                          <div className="rounded-xl bg-emerald-500/10 p-3">
                            <Brain className="text-emerald-400" size={21} />
                          </div>
                          <div>
                            <h3 className={`font-semibold ${primaryText}`}>
                              Double Machine Learning
                            </h3>
                            <p className="text-xs text-slate-500">
                              Synthetic validation
                            </p>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="flex items-center justify-between border-b border-slate-700/50 pb-3">
                            <span className="text-sm text-slate-400">
                              Holdout true ATE
                            </span>
                            <span className="font-semibold text-white">
                              {apiData?.modelInsights?.primary_validation?.true_ate?.toFixed(6) ?? "Loading..."}
                            </span>
                          </div>
                          <div className="flex items-center justify-between border-b border-slate-700/50 pb-3">
                            <span className="text-sm text-slate-400">
                              Holdout estimated ATE
                            </span>
                            <span className="font-semibold text-emerald-400">
                              {apiData?.modelInsights?.primary_validation?.estimated_ate?.toFixed(6) ?? "Loading..."}
                            </span>
                          </div>
                          <div className="flex items-center justify-between border-b border-slate-700/50 pb-3">
                            <span className="text-sm text-slate-400">
                              Holdout MAE
                            </span>
                            <span className="font-semibold text-white">
                              {apiData?.modelInsights?.primary_validation?.mae?.toFixed(6) ?? "Loading..."}
                            </span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm text-slate-400">
                              Holdout RMSE
                            </span>
                            <span className="font-semibold text-white">
                              {apiData?.modelInsights?.primary_validation?.rmse?.toFixed(6) ?? "Loading..."}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className={`rounded-2xl border p-5 ${cardBackground}`}>
                        <div className="mb-5 flex items-center gap-3">
                          <div className="rounded-xl bg-amber-500/10 p-3">
                            <ShieldAlert className="text-amber-400" size={21} />
                          </div>
                          <div>
                            <h3 className={`font-semibold ${primaryText}`}>
                              Model limitations
                            </h3>
                            <p className="text-xs text-slate-500">
                              Important considerations
                            </p>
                          </div>
                        </div>

                        <ul className="space-y-4 text-sm text-slate-400">
                          <li className="flex gap-3">
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-amber-400" />
                            Pricing analysis uses synthetic data and assumptions.
                          </li>
                          <li className="flex gap-3">
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-amber-400" />
                            Online Retail analysis is observational and cannot
                            establish causal effects.
                          </li>
                          <li className="flex gap-3">
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-amber-400" />
                            Conversion classifier performance is limited.
                          </li>
                          <li className="flex gap-3">
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-amber-400" />
                            No live business experiment or automated model
                            retraining is implemented.
                          </li>
                        </ul>
                      </div>
                    </div>

                    <div className="mt-6 rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">
                      <div className="flex items-center gap-2">
                        <CircleHelp className="text-blue-400" size={19} />
                        <h3 className="font-semibold text-blue-400">
                          How to interpret these results
                        </h3>
                      </div>
                      <p className="mt-3 text-sm leading-6 text-slate-400">
                        Model metrics describe performance on the datasets
                        used for evaluation. Synthetic validation checks
                        whether the method can recover a known treatment
                        effect under controlled assumptions. Real-world
                        deployment requires additional validation using
                        relevant business data and experiments.
                      </p>
                    </div>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>

            {/* Footer */}
            <footer className="mt-12 border-t border-slate-800 pt-6">
              <div className="flex flex-col justify-between gap-3 text-xs text-slate-500 sm:flex-row">
                <p>
                  © 2026 EconoCausal · Dynamic Pricing & Causal Analytics
                </p>
                <p className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-emerald-400" />
                  Analytics dashboard
                </p>
              </div>
              <p className="mt-3 max-w-3xl text-[11px] leading-5 text-slate-600">
                This dashboard is a decision-support interface. Results are
                based on experimental, synthetic and observational datasets.
                They should not be interpreted as guaranteed business
                outcomes. The displayed frontend metrics are illustrative
                project results and are not yet connected to a live backend API.
              </p>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}
