# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://mango.markets/) support is available at:
#   [Docs](https://docs.mango.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import logging
import multiprocessing
import requests
import time
import typing

from decimal import Decimal
from rx.scheduler.threadpoolscheduler import ThreadPoolScheduler
from solana.publickey import PublicKey
from solana.rpc.commitment import Commitment

from .client import BetterClient, ClusterUrlData, TransactionStatusCollector, NullTransactionStatusCollector
from .constants import MangoConstants
from .instructionreporter import InstructionReporter, CompoundInstructionReporter
from .instrumentlookup import InstrumentLookup
from .marketlookup import MarketLookup
from .text import indent_collection_as_str, indent_item_by


# # 🥭 Context class
#
# A `Context` object to manage Solana connection and Mango configuration.
#
class Context:
    def __init__(self, name: str, cluster_name: str, cluster_urls: typing.Sequence[ClusterUrlData], skip_preflight: bool,
                 commitment: str, encoding: str, blockhash_cache_duration: int, http_request_timeout: float,
                 stale_data_pauses_before_retry: typing.Sequence[float], mango_program_address: PublicKey,
                 serum_program_address: PublicKey, group_name: str, group_address: PublicKey,
                 gma_chunk_size: Decimal, gma_chunk_pause: Decimal, instrument_lookup: InstrumentLookup,
                 market_lookup: MarketLookup, transaction_status_collector: TransactionStatusCollector = NullTransactionStatusCollector()) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.name: str = name
        instruction_reporter: InstructionReporter = CompoundInstructionReporter.from_addresses(
            mango_program_address, serum_program_address)
        self.client: BetterClient = BetterClient.from_configuration(name, cluster_name, cluster_urls, Commitment(
            commitment), skip_preflight, encoding, blockhash_cache_duration, http_request_timeout, stale_data_pauses_before_retry, instruction_reporter, transaction_status_collector)
        self.mango_program_address: PublicKey = mango_program_address
        self.serum_program_address: PublicKey = serum_program_address
        self.group_name: str = group_name
        self.group_address: PublicKey = group_address
        self.gma_chunk_size: Decimal = gma_chunk_size
        self.gma_chunk_pause: Decimal = gma_chunk_pause
        self.instrument_lookup: InstrumentLookup = instrument_lookup
        self.market_lookup: MarketLookup = market_lookup

        self.ping_interval: int = 10

        self._last_generated_client_id: int = 0

        # kangda said in Discord: https://discord.com/channels/791995070613159966/836239696467591186/847816026245693451
        # "I think you are better off doing 4,8,16,20,30"
        self.retry_pauses: typing.Sequence[Decimal] = [Decimal(4), Decimal(
            8), Decimal(16), Decimal(20), Decimal(30)]

    def create_thread_pool_scheduler(self) -> ThreadPoolScheduler:
        return ThreadPoolScheduler(multiprocessing.cpu_count())

    def generate_client_id(self) -> int:
        # Previously used a random client ID strategy, which may be appropriate for some people.
        #   9223372036854775807 is sys.maxsize for 64-bit systems, with a bit_length of 63.
        #   We explicitly want to use a max of 64-bits though, so we use the number instead of
        #   sys.maxsize, which could be lower on 32-bit systems or higher on 128-bit systems.
        # return random.randrange(9223372036854775807)
        #
        # After this discussion with Max on Discord (https://discord.com/channels/791995070613159966/818978757648842782/884751007656054804):
        #   can you generate monotonic ids?
        #   in case not the result wouldn't be different from what we have rn, which is random display
        #   so there's still a net benefit for changing the UI
        #   and if you could use the same id generation scheme (unix time in ms) it would even work well with the UI :slight_smile:
        #
        # We go with the time in milliseconds. We get the time in nanoseconds and divide it by 1,000,000 to get
        # the time in milliseconds.
        #
        # But there's more! Because this can be called in a burst, for, say, a dozen orders all within the same
        # millisecond. And using duplicate client order IDs would be Bad. So we keep track of the last one we
        # sent, and we just add one if we get an identical value.
        new_id: int = round(time.time_ns() / 1000000)
        if new_id <= self._last_generated_client_id:
            new_id = self._last_generated_client_id + 1
        self._last_generated_client_id = new_id
        return new_id

    def lookup_group_name(self, group_address: PublicKey) -> str:
        group_address_str = str(group_address)
        for group in MangoConstants["groups"]:
            if group["cluster"] == self.client.cluster_name and group["publicKey"] == group_address_str:
                return str(group["name"])

        return "« Unknown Group »"

    def fetch_stats(self, url_suffix: str) -> typing.Sequence[typing.Any]:
        stats_url = f"https://mango-stats-v3.herokuapp.com/{url_suffix}"
        stats_response = requests.get(stats_url)
        return typing.cast(typing.Sequence[typing.Any], stats_response.json())

    def __str__(self) -> str:
        cluster_urls: str = indent_item_by(indent_collection_as_str(self.client.cluster_urls))
        return f"""« Context '{self.name}':
    Cluster Name: {self.client.cluster_name}
    Cluster URLs:
        {cluster_urls}
    Group Name: {self.group_name}
    Group Address: {self.group_address}
    Mango Program Address: {self.mango_program_address}
    Serum Program Address: {self.serum_program_address}
»"""

    def __repr__(self) -> str:
        return f"{self}"
