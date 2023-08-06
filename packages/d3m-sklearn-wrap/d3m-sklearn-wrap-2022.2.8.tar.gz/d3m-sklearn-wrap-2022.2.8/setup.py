import os
from setuptools import setup, find_packages

PACKAGE_NAME = 'sklearn_wrap'
PUBLISHED_NAME = 'd3m-sklearn-wrap'


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert False, "'{0}' not found in '{1}'".format(key, module_path)


setup(
    name=PUBLISHED_NAME,
    version=read_package_variable('__version__'),
    license="Apache-2.0",
    description='Primitives created using the Sklearn auto wrapper',
    author=read_package_variable('__author__'),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'd3m',
        'scikit-learn>=0.21.3,<0.24',
    ],
    url='https://gitlab.com/datadrivendiscovery/sklearn-wrap',
    entry_points = {
        'd3m.primitives': [
            'data_cleaning.string_imputer.SKlearn = sklearn_wrap.SKStringImputer:SKStringImputer',
            'classification.quadratic_discriminant_analysis.SKlearn = sklearn_wrap.SKQuadraticDiscriminantAnalysis:SKQuadraticDiscriminantAnalysis',
            'classification.random_forest.SKlearn = sklearn_wrap.SKRandomForestClassifier:SKRandomForestClassifier',
            'classification.ada_boost.SKlearn = sklearn_wrap.SKAdaBoostClassifier:SKAdaBoostClassifier',
            'classification.nearest_centroid.SKlearn = sklearn_wrap.SKNearestCentroid:SKNearestCentroid',
            'classification.gaussian_naive_bayes.SKlearn = sklearn_wrap.SKGaussianNB:SKGaussianNB',
            'classification.decision_tree.SKlearn = sklearn_wrap.SKDecisionTreeClassifier:SKDecisionTreeClassifier',
            'classification.linear_svc.SKlearn = sklearn_wrap.SKLinearSVC:SKLinearSVC',
            'classification.svc.SKlearn = sklearn_wrap.SKSVC:SKSVC',
            'classification.mlp.SKlearn = sklearn_wrap.SKMLPClassifier:SKMLPClassifier',
            'classification.linear_discriminant_analysis.SKlearn = sklearn_wrap.SKLinearDiscriminantAnalysis:SKLinearDiscriminantAnalysis',
            'classification.logistic_regression.SKlearn = sklearn_wrap.SKLogisticRegression:SKLogisticRegression',
            'classification.bernoulli_naive_bayes.SKlearn = sklearn_wrap.SKBernoulliNB:SKBernoulliNB',
            'classification.dummy.SKlearn = sklearn_wrap.SKDummyClassifier:SKDummyClassifier',
            'classification.passive_aggressive.SKlearn = sklearn_wrap.SKPassiveAggressiveClassifier:SKPassiveAggressiveClassifier',
            'classification.k_neighbors.SKlearn = sklearn_wrap.SKKNeighborsClassifier:SKKNeighborsClassifier',
            'classification.multinomial_naive_bayes.SKlearn = sklearn_wrap.SKMultinomialNB:SKMultinomialNB',
            'classification.bagging.SKlearn = sklearn_wrap.SKBaggingClassifier:SKBaggingClassifier',
            'classification.sgd.SKlearn = sklearn_wrap.SKSGDClassifier:SKSGDClassifier',
            'classification.extra_trees.SKlearn = sklearn_wrap.SKExtraTreesClassifier:SKExtraTreesClassifier',
            'classification.gradient_boosting.SKlearn = sklearn_wrap.SKGradientBoostingClassifier:SKGradientBoostingClassifier',
            'regression.kernel_ridge.SKlearn = sklearn_wrap.SKKernelRidge:SKKernelRidge',
            'regression.ada_boost.SKlearn = sklearn_wrap.SKAdaBoostRegressor:SKAdaBoostRegressor',
            'regression.passive_aggressive.SKlearn = sklearn_wrap.SKPassiveAggressiveRegressor:SKPassiveAggressiveRegressor',
            'regression.lars.SKlearn = sklearn_wrap.SKLars:SKLars',
            'regression.gradient_boosting.SKlearn = sklearn_wrap.SKGradientBoostingRegressor:SKGradientBoostingRegressor',
            'regression.mlp.SKlearn = sklearn_wrap.SKMLPRegressor:SKMLPRegressor',
            'regression.linear.SKlearn = sklearn_wrap.SKLinearRegression:SKLinearRegression',
            'regression.lasso.SKlearn = sklearn_wrap.SKLasso:SKLasso',
            'regression.extra_trees.SKlearn = sklearn_wrap.SKExtraTreesRegressor:SKExtraTreesRegressor',
            'regression.bagging.SKlearn = sklearn_wrap.SKBaggingRegressor:SKBaggingRegressor',
            'regression.random_forest.SKlearn = sklearn_wrap.SKRandomForestRegressor:SKRandomForestRegressor',
            'regression.linear_svr.SKlearn = sklearn_wrap.SKLinearSVR:SKLinearSVR',
            'regression.ard.SKlearn = sklearn_wrap.SKARDRegression:SKARDRegression',
            'regression.ridge.SKlearn = sklearn_wrap.SKRidge:SKRidge',
            'regression.k_neighbors.SKlearn = sklearn_wrap.SKKNeighborsRegressor:SKKNeighborsRegressor',
            'regression.dummy.SKlearn = sklearn_wrap.SKDummyRegressor:SKDummyRegressor',
            'regression.lasso_cv.SKlearn = sklearn_wrap.SKLassoCV:SKLassoCV',
            'regression.elastic_net.SKlearn = sklearn_wrap.SKElasticNet:SKElasticNet',
            'regression.sgd.SKlearn = sklearn_wrap.SKSGDRegressor:SKSGDRegressor',
            'regression.gaussian_process.SKlearn = sklearn_wrap.SKGaussianProcessRegressor:SKGaussianProcessRegressor',
            'regression.svr.SKlearn = sklearn_wrap.SKSVR:SKSVR',
            'regression.decision_tree.SKlearn = sklearn_wrap.SKDecisionTreeRegressor:SKDecisionTreeRegressor',
            'feature_extraction.feature_agglomeration.SKlearn = sklearn_wrap.SKFeatureAgglomeration:SKFeatureAgglomeration',
            'data_cleaning.imputer.SKlearn = sklearn_wrap.SKImputer:SKImputer',
            'feature_selection.select_fwe.SKlearn = sklearn_wrap.SKSelectFwe:SKSelectFwe',
            'data_cleaning.normalizer.SKlearn = sklearn_wrap.SKNormalizer:SKNormalizer',
            'data_cleaning.binarizer.SKlearn = sklearn_wrap.SKBinarizer:SKBinarizer',
            'data_cleaning.quantile_transformer.SKlearn = sklearn_wrap.SKQuantileTransformer:SKQuantileTransformer',
            'feature_extraction.truncated_svd.SKlearn = sklearn_wrap.SKTruncatedSVD:SKTruncatedSVD',
            'feature_selection.variance_threshold.SKlearn = sklearn_wrap.SKVarianceThreshold:SKVarianceThreshold',
            'feature_extraction.kernel_pca.SKlearn = sklearn_wrap.SKKernelPCA:SKKernelPCA',
            'data_transformation.one_hot_encoder.SKlearn = sklearn_wrap.SKOneHotEncoder:SKOneHotEncoder',
            'feature_extraction.pca.SKlearn = sklearn_wrap.SKPCA:SKPCA',
            'data_transformation.ordinal_encoder.SKlearn = sklearn_wrap.SKOrdinalEncoder:SKOrdinalEncoder',
            'data_cleaning.standard_scaler.SKlearn = sklearn_wrap.SKStandardScaler:SKStandardScaler',
            'data_transformation.gaussian_random_projection.SKlearn = sklearn_wrap.SKGaussianRandomProjection:SKGaussianRandomProjection',
            'feature_extraction.tfidf_vectorizer.SKlearn = sklearn_wrap.SKTfidfVectorizer:SKTfidfVectorizer',
            'data_cleaning.robust_scaler.SKlearn = sklearn_wrap.SKRobustScaler:SKRobustScaler',
            'data_transformation.nystroem.SKlearn = sklearn_wrap.SKNystroem:SKNystroem',
            'data_transformation.random_trees_embedding.SKlearn = sklearn_wrap.SKRandomTreesEmbedding:SKRandomTreesEmbedding',
            'data_cleaning.missing_indicator.SKlearn = sklearn_wrap.SKMissingIndicator:SKMissingIndicator',
            'data_transformation.polynomial_features.SKlearn = sklearn_wrap.SKPolynomialFeatures:SKPolynomialFeatures',
            'data_cleaning.min_max_scaler.SKlearn = sklearn_wrap.SKMinMaxScaler:SKMinMaxScaler',
            'feature_selection.select_percentile.SKlearn = sklearn_wrap.SKSelectPercentile:SKSelectPercentile',
            'data_transformation.sparse_random_projection.SKlearn = sklearn_wrap.SKSparseRandomProjection:SKSparseRandomProjection',
            'data_transformation.fast_ica.SKlearn = sklearn_wrap.SKFastICA:SKFastICA',
            'data_transformation.rbf_sampler.SKlearn = sklearn_wrap.SKRBFSampler:SKRBFSampler',
            'feature_extraction.count_vectorizer.SKlearn = sklearn_wrap.SKCountVectorizer:SKCountVectorizer',
            'data_cleaning.max_abs_scaler.SKlearn = sklearn_wrap.SKMaxAbsScaler:SKMaxAbsScaler',
            'feature_selection.generic_univariate_select.SKlearn = sklearn_wrap.SKGenericUnivariateSelect:SKGenericUnivariateSelect',
        ],
    },
)