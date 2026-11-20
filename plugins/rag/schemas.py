from typing import List, Optional

from pydantic import BaseModel

S = Optional[str]  # all values kept as source strings; None/"" = absent in the article


class Publication(BaseModel):
    title: S = None
    year: S = None
    DOI: S = None
    authors: S = None  # separated by '; '
    in_scope: bool
    exclusion_reason: S = None


class Configuration(BaseModel):
    config_id: str
    rag_variant: S = None
    retrieval_method: S = None
    retriever_model: S = None
    embedding_model: S = None
    embedding_version: S = None
    chunking_method: S = None
    chunk_size: S = None
    chunk_overlap: S = None
    chunk_unit: S = None
    index_type: S = None
    vector_store: S = None
    top_k: S = None
    reranker_model: S = None
    generator_model: S = None
    generator_version: S = None
    prompt_strategy: S = None
    context_strategy: S = None
    note: S = None


class Dataset(BaseModel):
    dataset_id: str
    dataset_name: S = None
    dataset_version: S = None
    language: S = None
    data_split: S = None
    scientific_domain: S = None
    note: S = None


class Task(BaseModel):
    task_id: str
    task_type: S = None
    note: S = None


class Experiment(BaseModel):
    experiment_id: str
    evaluation_protocol: S = None
    baseline_name: S = None
    hardware: S = None
    latency_ms: S = None
    tokens_per_query: S = None
    sample_size: S = None
    note: S = None


class Result(BaseModel):
    result_id: str
    experiment_id: S = None
    config_id: S = None
    dataset_id: S = None
    task_id: S = None
    metric_group: S = None
    metric_name: S = None
    metric_variant: S = None
    metric_direction: S = None
    metric_k: S = None
    metric_value: S = None
    metric_unit: S = None
    baseline_value: S = None
    aggregation: S = None
    sample_size: S = None
    raw_value: S = None
    raw_unit: S = None
    normalized_value: S = None
    normalized_unit: S = None
    result_origin: S = None  # primary | cited
    cited_publication_id: S = None
    source_page: S = None
    source_section: S = None
    source_table: S = None
    source_figure: S = None
    source_fragment: S = None
    extraction_status: S = None  # extracted | present_not_extractable | absent
    duplicate_of: S = None
    note: S = None


class Issue(BaseModel):
    issue_id: str
    record_ids: S = None  # result_ids separated by ';'
    check_name: S = None
    description: S = None
    source_page: S = None
    source_fragment: S = None


class PaperExtraction(BaseModel):
    publication: Publication
    configurations: List[Configuration] = []
    datasets: List[Dataset] = []
    tasks: List[Task] = []
    experiments: List[Experiment] = []
    results: List[Result] = []
    issues: List[Issue] = []
