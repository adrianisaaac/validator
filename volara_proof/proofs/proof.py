import copy

from volara_proof.extract import extract_data
from volara_proof.proofs.proof_of_quality import proof_of_quality
from volara_proof.models.proof_response import ProofResponse
from volara_proof.models.proof_config import ProofConfig

from volara_proof.storage.rewards import RewardsStorage

rewards_storage = RewardsStorage()


def proof(
    input_file: str, proof_response: ProofResponse, config: ProofConfig
) -> ProofResponse:
    proof_response = copy.deepcopy(proof_response)
    tweets_data = extract_data(input_file)
    is_valid, file_score, tweet_info, unique_tweets, total_tweets = (
        proof_of_quality(tweets_data, config.file_id, config)
    ).values()
    proof_response.valid = is_valid
    proof_response.score = file_score
    proof_response.authenticity = 0
    proof_response.ownership = 0
    proof_response.quality = file_score
    proof_response.uniqueness = unique_tweets / total_tweets if total_tweets > 0 else 0
    if is_valid and file_score > 0:
        rewards_storage.post_rewards(
            config.file_id, config.miner_address, file_score, tweet_info
        )
    return proof_response
