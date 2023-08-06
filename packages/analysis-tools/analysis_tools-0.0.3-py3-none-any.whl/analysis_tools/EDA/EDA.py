from analysis_tools.common.util import *
from sklearn import ensemble
from sklearn.inspection import permutation_importance


class EDA:
    class FigSaver(ContextDecorator):
        def __init__(self, path):
            if path is not None:
                self.path = join(path, 'EDA')
                os.makedirs(self.path, exist_ok=True)
            else:
                self.path = None
        def update(self, title, fig, options={}, tight_layout=True):
            self.title        = title
            self.fig          = fig
            self.options      = options
            self.tight_layout = tight_layout
            return self
        def __enter__(self):
            pass
        def __exit__(self, *exc):
            if self.tight_layout:
                self.fig.suptitle(self.title, **self.options)
                self.fig.tight_layout()
            if self.path:
                self.fig.savefig(join(self.path, f"{self.title}.png"))
            plt.show()

    def __init__(self, data, target, save_path=None):
        self.target = target
        self.set_plot_options(save_path)
        self.update(data)

    ''
    ### Main method #########################################
    def set_types(self, ord=(), nom=()):
        def inference_types(ord, nom):
            types = dict()
            dtypes = self.data.dtypes
            for f in self.data:
                if f in ord:
                    types[f] = 'ord'
                    self.data[f] = self.data[f].map(lambda x: str(x) if pd.notnull(x) else None)
                elif dtypes[f] == 'object' or f in nom:
                    types[f] = 'nom'
                    self.data[f] = self.data[f].map(lambda x: str(x) if pd.notnull(x) else None)
                else:
                    types[f] = 'num'
            return types
        self.types = inference_types(ord, nom)
        dtypes = self.data.dtypes.to_frame(name='dtype')
        dtypes['type'] = [self.types[k] for k in dtypes.index]
        display(dtypes.T)
    def run(self, fixed_feature=None):
        fixed_feature = fixed_feature if fixed_feature else self.target
        self.missing_value(self.data)
        self.corr(self.data)
        self.pairplot(self.data)
        for f in [f for f in self.data.columns if f != fixed_feature]:
            self.compare_features(self.data, f, fixed_feature)
    def missing_value(self, data):
        fig, axes = plt.subplots(2, 1)
        with self.figsaver.update("Missing value in full data", fig):
            missingno.matrix(data, ax=axes[0])
            ms = data.isnull().sum()
            sns.barplot(ms.index, ms, ax=axes[1])
            axes[1].bar_label(axes[1].containers[0])
            axes[1].set_xticklabels([])
    def corr(self, data):
        data = self.select_num_features(data)
        with self.figsaver.update("Correlation between numerical features", plt.figure()):
            corr = data.corr()
            sns.heatmap(corr, mask=np.eye(len(corr)), annot=True, center=0, fmt='.2f', cmap='coolwarm')
    def pairplot(self, data):
        data = self.select_num_features(data)
        options = {} if self.types[self.target] == 'num' else {'hue': self.target}
        g = sns.pairplot(data.reset_index(drop=True), kind='reg', palette='Set1', **options)
        with self.figsaver.update("Pairplot between numerical features", g.fig, tight_layout=False):
            pass
    def explore_feature(self, data, f=None, type=None, axes=None):
        type = type if type else self.types[f]

        if type == 'num':
            def plot(values, ax1, ax2):
                stats = boxplot_stats(values[values.notnull()])[0]
                sns.boxplot(values, ax=ax1)
                sns.histplot(values, ax=ax2, bins=50, kde=True, stat='density')
                text = f"""whislo({stats['whislo']:.2f}), Q1({stats['q1']:.2f}), med({stats['med']:.2f}), Q3({stats['q3']:.2f}), whishi({stats['whishi']:.2f})
                           min({min(values):.2f}), max({max(values):.2f})"""
                ax1.text(1, -0.05, text, ha='right', va='top', transform=ax1.transAxes, fontsize=15)
                ax1.set_xlabel(None);  ax1.set_xticklabels([])
        elif type in ['ord', 'nom']:
            def values2count(values, type):
                count = values.value_counts().head(self.max_n_class)
                return count.sort_index() if type == 'ord' else count
            def plot(values, ax1, ax2):
                count = values2count(values, type)
                count.plot.pie(radius=2, explode=[0.05]*len(count), autopct='%1.1f%%', ax=ax1);  ax1.set_ylabel(None)
                sns.countplot(values, ax=ax2, order=count.index)
                for p in ax2.patches:  # add annotation
                    x = p.get_bbox().get_points()[:, 0]
                    y = p.get_bbox().get_points()[1, 1]
                    ax2.annotate(int(y), (x.mean(), y), ha='center', va='bottom', fontsize=15)
        else:
            raise ValueError(type)

        values = data[f] if f else data
        if axes:
            ax1, ax2 = axes
            plot(values, ax1, ax2)
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1)
            with self.figsaver.update(self._get_title(values, type), fig):
                plot(values, ax1, ax2)

        if type in ['ord', 'nom']:
            return values2count(values, type).index
    def compare_features(self, data, f1, f2):
        return eval(f"self.compare_{self.types[f1]}_{self.types[f2]}")(data, f1, f2)

    def compare_num_num(self, data, f1, f2):
        t1, t2 = 'num', 'num'
        fig, (axes0, axes1, ax2) = self._get_grid32()
        with self.figsaver.update(f"{self._get_title(data[f1], t1)} \n {self._get_title(data[f2], t2)}", fig):
            self.explore_feature(data, f1, t1, (axes0[0], axes1[0]))
            self.explore_feature(data, f2, t2, (axes0[1], axes1[1]))
            sns.regplot(data[f1], data[f2], ax=ax2, marker='x', scatter_kws={'alpha': 0.5}, label=f"corr: {data.corr().loc[f1, f2]:.2f}")
            ax2.legend()
    def compare_num_cat(self, data, f1, f2, t1, t2):
        fig, (axes0, axes1, ax2, ax3, ax4) = self._get_grid52()
        with self.figsaver.update(f"{self._get_title(data[f1], t1)} \n {self._get_title(data[f2], t2)}", fig):
            self.explore_feature(data, f1, t1, (axes0[0], axes1[0]))
            order = self.explore_feature(data, f2, t2, (axes0[1], axes1[1]))
            sns.boxplot(x=f1, y=f2, data=data, ax=ax2, orient='h', order=order)
            sns.stripplot(x=f1, y=f2, data=data, ax=ax3, alpha=0.3, orient='h', order=order).set_xlim(ax2.set_xlim())
            sns.histplot(x=f1, hue=f2, data=data, bins=100, kde=True, ax=ax4, hue_order=order, stat='density').set_xlim(ax2.set_xlim())
            for ax in (ax2, ax3):
                ax.set_xlabel(None);  ax.set_xticklabels([])
    def compare_cat_num(self, data, f1, f2, t1, t2):
        fig, (axes0, axes1, ax2, ax3) = self._get_grid42()
        with self.figsaver.update(f"{self._get_title(data[f1], t1)} \n {self._get_title(data[f2], t2)}", fig):
            order = self.explore_feature(data, f1, t1, (axes0[0], axes1[0]))
            self.explore_feature(data, f2, t2, (axes0[1], axes1[1]))
            sns.boxplot(x=f1, y=f2, data=data, ax=ax2, order=order)
            sns.swarmplot(x=f1, y=f2, data=data, ax=ax3, alpha=0.3, order=order).set_ylim(ax2.set_ylim())
            ax2.set_xlabel(None);  ax2.set_xticklabels([])
    def compare_num_ord(self, data, f1, f2):
        self.compare_num_cat(data, f1, f2, 'num', 'ord')
    def compare_ord_num(self, data, f1, f2):
        return self.compare_cat_num(data, f1, f2, 'ord', 'num')
    def compare_num_nom(self, data, f1, f2):
        self.compare_num_cat(data, f1, f2, 'num', 'nom')
    def compare_nom_num(self, data, f1, f2):
        return self.compare_cat_num(data, f1, f2, 'nom', 'num')
    def compare_cat_cat(self, data, f1, f2, t1, t2):
        fig, (axes0, axes1, ax2) = self._get_grid32()
        with self.figsaver.update(f"{self._get_title(data[f1], t1)} \n {self._get_title(data[f2], t2)}", fig):
            order1 = self.explore_feature(data, f1, t1, (axes0[0], axes1[0]))
            order2 = self.explore_feature(data, f2, t2, (axes0[1], axes1[1]))
            count = pd.crosstab(data[f1][data[f1].isin(order1)], data[f2][data[f2].isin(order2)])
            ratio = count / count.values.sum()
            ratio['order1'] = ratio.index.map(lambda idx: order1.get_loc(idx))
            ratio.sort_values('order1', inplace=True)  # sort by order1
            ratio.drop(columns=['order1'], inplace=True)
            ratio = ratio[[f for f in ratio.columns if f in order2]]  # sort by order2
            sns.heatmap(ratio, annot=True, fmt=".2f", cmap=sns.light_palette('gray', as_cmap=True), ax=ax2)
            ax2.set_ylabel(f1)
    def compare_ord_ord(self, data, f1, f2):
        return self.compare_cat_cat(data, f1, f2, 'ord', 'ord')
    def compare_ord_nom(self, data, f1, f2):
        return self.compare_cat_cat(data, f1, f2, 'ord', 'nom')
    def compare_nom_ord(self, data, f1, f2):
        return self.compare_cat_cat(data, f1, f2, 'nom', 'ord')
    def compare_nom_nom(self, data, f1, f2):
        return self.compare_cat_cat(data, f1, f2, 'nom', 'nom')

    def get_feature_importance(self, X, y, problem='classification', plot_n_feature=20):
        ## 1. Model
        options = {'n_jobs': -1}
        if problem == 'classification':
            model = ensemble.RandomForestClassifier(**options)
        else:
            model = ensemble.RandomForestRegressor(**options)
        model.fit(X, y)

        ## 2. Get feature importance
        MDI_importance  = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        perm_importance = pd.Series(permutation_importance(model, X, y, **options).importances_mean, index=X.columns).sort_values(ascending=False)

        ## 3. Mean importance
        fi1             = pd.Series(range(len(MDI_importance)), index=MDI_importance.index)
        fi2             = pd.Series(range(len(perm_importance)), index=perm_importance.index)
        mean_importance = (fi1 + fi2).sort_values()

        ## 4. Plot
        fig, axes = plt.subplots(3, 1, figsize=(20, 20))
        MDI_importance_plot  = MDI_importance.head(plot_n_feature)
        perm_importance_plot = perm_importance.head(plot_n_feature)
        mean_importance_plot = mean_importance.head(plot_n_feature)
        sns.barplot(MDI_importance_plot.index, MDI_importance_plot, ax=axes[0])
        sns.barplot(perm_importance_plot.index, perm_importance_plot, ax=axes[1])
        sns.barplot(mean_importance_plot.index, mean_importance_plot, ax=axes[2])
        axes[0].set_ylabel("Mean decrease in impurity")
        axes[1].set_ylabel("Mean accuracy decrease")
        axes[2].set_ylabel("Mean rank")
        axes[0].set_title("Feature importance using MDI")
        axes[1].set_title("Feature importance using permutation on full model")
        axes[2].set_title("Feature importance using MDI, permutation on full model")
        for ax in axes:
            ax.tick_params(axis='x', rotation=30)
        fig.tight_layout()
        plt.show()

        # return MDI_importance, perm_importance, mean_importance,
        return mean_importance
    #########################################################


    ''
    ### Sub method ########################################
    def update(self, data=None, ord=(), nom=()):
        self.data = data.copy()
        self.overview(self.data)
        self.set_types(ord, nom)
    def overview(self, data):
        display_md(f"# Full data{data.shape}: train{data[data[self.target].notnull()].shape} + test{data[data[self.target].isnull()].shape}")
        display(data.head())
    def select_num_features(self, data):
        rst = pd.DataFrame()
        for f in data:
            try:
                rst = pd.concat([rst, data[f].astype(float)], axis='columns')
            except:
                pass
        return rst
    def set_plot_options(self, save_path):
        self.figsaver       = self.FigSaver(save_path)
        self.max_n_class    = 5
        figsize_default     = plt.rcParams['figure.figsize']
        self.figsize_grid32 = (figsize_default[0], 1.5*figsize_default[1])
        self.figsize_grid42 = (figsize_default[0], 2.0*figsize_default[1])
        self.figsize_grid52 = (figsize_default[0], 2.5*figsize_default[1])


    ## Utility methods
    def _get_grid32(self):
        gs    = GridSpec(3, 2, height_ratios=[1, 1, 3])
        fig   = plt.figure(figsize=self.figsize_grid32)
        axes0 = (fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]))  # row 0
        axes1 = (fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1]))  # row 1
        ax2   = fig.add_subplot(gs[2, :])                               # row 2
        return fig, (axes0, axes1, ax2)
    def _get_grid42(self):
        gs    = GridSpec(4, 2, height_ratios=[1, 1, 2, 2])
        fig   = plt.figure(figsize=self.figsize_grid42)
        axes0 = (fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]))  # row 0
        axes1 = (fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1]))  # row 1
        ax2   = fig.add_subplot(gs[2, :])                               # row 2
        ax3   = fig.add_subplot(gs[3, :])                               # row 2
        return fig, (axes0, axes1, ax2, ax3)
    def _get_grid52(self):
        gs    = GridSpec(5, 2, height_ratios=[1, 1, 1, 1, 2])
        fig   = plt.figure(figsize=self.figsize_grid52)
        axes0 = (fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]))  # row 0
        axes1 = (fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1]))  # row 1
        ax2   = fig.add_subplot(gs[2, :])                               # row 2
        ax3   = fig.add_subplot(gs[3, :])                               # row 3
        ax4   = fig.add_subplot(gs[4, :])                               # row 4
        return fig, (axes0, axes1, ax2, ax3, ax4)
    def _get_title(self, ser, type):
        n_miss = f"miss({ser.isna().sum()} in {len(ser)})"
        if type != 'num':  # categorical
            n_unique = f"unique({ser.nunique()})"
            title = ' | '.join([ser.name, type, n_miss, n_unique])
        else:
            title = ' | '.join([ser.name, type, n_miss])
        return title
    #########################################################
