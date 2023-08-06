__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import textwrap
import pandas as pd
from mclumi.util.Writer import writer as gwriter
from mclumi.util.Reader import reader as gfreader
from mclumi.util.Number import number as rannum
from mclumi.Path import to
from mclumi.align.Read import read as aliread
from mclumi.util.Console import console
from mclumi.util.Hamming import hamming


class umiTranslocSelf():

    def __init__(self, metric, method, umi_lib_fpn=None, fastq_fp=None, is_self_healing=False, is_dedup=False):
        super(umiTranslocSelf, self).__init__()
        self.metric = metric
        self.gfreader = gfreader()
        self.gwriter = gwriter()
        self.rannum = rannum()
        self.umi_lib_fpn = umi_lib_fpn
        self.method = method
        self.seq_num = 100
        df_dedup = pd.DataFrame()
        df_fake_sgl_est = pd.DataFrame()
        df_fake_sgl_act = pd.DataFrame()
        df_real_sgl_est = pd.DataFrame()
        df_real_sgl_act = pd.DataFrame()
        df_fake_bulk_est = pd.DataFrame()
        df_fake_bulk_act = pd.DataFrame()
        df_real_bulk_est = pd.DataFrame()
        df_real_bulk_act = pd.DataFrame()

        self.df_ref_umi = self.gfreader.generic(df_fpn=self.umi_lib_fpn)[0].values
        self.df_ref_umi = pd.DataFrame.from_dict({i: e for i, e in enumerate(self.df_ref_umi)}, orient='index', columns=['raw'])
        self.df_ref_umi['index'] = self.df_ref_umi.index
        self.df_ref_umi['collap'] = self.df_ref_umi['raw'].apply(lambda x: ''.join([i[0] for i in textwrap.wrap(x, 3)]))
        self.umi_collap_map = {i: e for i, e in enumerate(self.df_ref_umi['collap'])}

        # reads = np.reshape(self.df_ref_umi[['collap', 'index']].values.tolist(), (int(self.seq_num / 2), 4))
        # print(pd.DataFrame(reads))
        est_fake_sgl_arr = []
        act_fake_sgl_arr = []
        est_real_sgl_arr = []
        act_real_sgl_arr = []
        est_fake_bulk_arr = []
        act_fake_bulk_arr = []
        est_real_bulk_arr = []
        act_real_bulk_arr = []
        dedup_arr = []
        self.console = console()
        self.console.verbose = self.verbose
        self.dirname = os.path.dirname(self.sv_fpn) + '/'

        self.alireader = aliread(
            bam_fpn=fastq_fp + self.metric + '/permute_' + '/bam/' + fn + '.bam',
            verbose=False,
        )
        self.df_bam = self.alireader.todf(tags=['PO'])
        self.df_bam['names'] = self.df_bam['query_name'].apply(lambda x: self.bamproc(x))

        self.df_bam['umi_l'] = self.df_bam['names'].apply(lambda x: x[-2])
        self.df_bam['umi_r'] = self.df_bam['names'].apply(lambda x: x[-1])
        self.df_bam['umi_corr_l'] = self.df_bam['umi_l'].apply(lambda x: self.correct(x))
        self.df_bam['umi_corr_r'] = self.df_bam['umi_r'].apply(lambda x: self.correct(x))
        self.df_fake = self.df_bam.loc[
            (self.df_bam['transloc_stat'] == 'fake_yes')
            # (self.df_bam['transloc_stat'] != 'real_yes')
            # & (self.df_bam['transloc_stat'] != 'real_no')
        ]
        print(self.df_fake)
        fake_sgl_num = self.df_fake.shape[0]
        act_fake_sgl_arr.append(fake_sgl_num)

        self.df_fake['r2_umi_ref'] = self.df_fake['r1_id'].apply(lambda x: self.umi_collap_map[int(x) + 1])
        # self.df_fake['cons'] = self.df_fake.apply(lambda x: self.screen1(x), axis=1)

        # est_fake_found_out_sgl_num = self.df_fake.loc[self.df_fake['cons'] == 0].shape[0]
        self.df_fake['hamm'] = self.df_fake.apply(lambda x: self.screen2(x), axis=1)
        scp = self.df_fake.loc[self.df_fake['hamm'] >= 6]
        # self.gwriter.generic(scp, sv_fpn=fastq_fp + 'asd')
        est_fake_found_out_sgl_num = scp.shape[0]
        # est_fake_sgl_num = fake_sgl_num - est_fake_found_out_sgl_num
        est_fake_sgl_num = est_fake_found_out_sgl_num
        est_fake_sgl_arr.append(est_fake_sgl_num)

        self.df_real = self.df_bam.loc[(self.df_bam['transloc_stat'] == 'real_yes')]
        real_sgl_num = self.df_real.shape[0]
        act_real_sgl_arr.append(real_sgl_num)
        self.df_real['r2_umi_ref'] = self.df_real['r1_id'].apply(lambda x: self.umi_collap_map[int(x) + 1])
        self.df_real['cons'] = self.df_real.apply(lambda x: self.screen1(x), axis=1)
        self.df_real['hamm'] = self.df_real.apply(lambda x: self.screen2(x), axis=1)
        est_real_found_out_sgl_num = self.df_real.loc[self.df_real['hamm'] <= 1].shape[0]
        # est_real_sgl_num = real_sgl_num - est_real_found_out_sgl_num
        est_real_sgl_num = est_real_found_out_sgl_num
        est_real_sgl_arr.append(est_real_sgl_num)
        print(real_sgl_num, est_real_sgl_num)

        df_fake_sgl_act['pn'] = act_fake_sgl_arr
        df_fake_sgl_est['pn'] = est_fake_sgl_arr
        df_real_sgl_act['pn'] = act_real_sgl_arr
        df_real_sgl_est['pn'] = est_real_sgl_arr
        df_fake_bulk_act['pn'] = act_fake_bulk_arr
        df_fake_bulk_est['pn'] = est_fake_bulk_arr
        df_real_bulk_act['pn'] = act_real_bulk_arr
        df_real_bulk_est['pn'] = est_real_bulk_arr
        df_dedup['pn'] = dedup_arr


        self.gwriter.generic(
            df=df_fake_sgl_act,
            sv_fpn=fastq_fp + self.metric + '/' + 'act_fake_healing_sgl' + '.txt',
            header=True,
        )
        self.gwriter.generic(
            df=df_fake_sgl_est,
            sv_fpn=fastq_fp + self.metric + '/' + 'est_fake_healing_sgl' + '.txt',
            header=True,
        )
        self.gwriter.generic(
            df=df_real_sgl_act,
            sv_fpn=fastq_fp + self.metric + '/' + 'act_real_healing_sgl' + '.txt',
            header=True,
        )
        self.gwriter.generic(
            df=df_real_sgl_est,
            sv_fpn=fastq_fp + self.metric + '/' + 'est_real_healing_sgl' + '.txt',
            header=True,
        )

    def screen(self, x):
        if x['r1_id'] != x['r2_id']:
            return 1
        else:
            return 0

    def screen1(self, x):
        if x['umi_corr_r'] != x['r2_umi_ref']:
            return 1
        else:
            return 0

    def screen2(self, x):
        return hamming().general(x['umi_corr_r'], x['r2_umi_ref'])

    def bamproc(self, x):
        t = x.split('-')
        # print(t)
        # print(x)
        tt = t[5].split('_')
        # print(t[0], t[1], t[2], t[3], t[4], tt[0], tt[1])
        return t[0], t[1], t[2], t[3], t[4], tt[0], tt[1]

    def correct(self, umi):
        vernier = [i for i in range(36) if i % 3 == 0]
        umi_trimers = [umi[v: v+3] for v in vernier]
        # umi_trimers = textwrap.wrap(umi, 3)
        t = []
        for umi_trimer in umi_trimers:
            s = set(umi_trimer)
            if len(s) == 3:
                rand_index = self.rannum.uniform(low=0, high=3, num=1, use_seed=False)[0]
                t.append(umi_trimer[rand_index])
            elif len(s) == 2:
                sdict = {umi_trimer.count(i): i for i in s}
                t.append(sdict[2])
            else:
                t.append(umi_trimer[0])
        return ''.join(t)

    def bamprocSlow(self, x):
        """
                self.df_bam[
                        ['read', 'r1_id', 'r2_id', 'transloc_stat', 'transloc_side', 'sam_id', 'source']
                    ] = self.df_bam.apply(lambda x: self.bamproc(x), axis=1)
        :param x:
        :return:
        """
        t = x['query_name'].split('-')
        # print(t)
        # print(x)
        tt = t[5].split('_')
        # print(t[0], t[1], t[2], t[3], t[4], tt[0], tt[1])
        return pd.Series({
            'read': t[0],
            'r1_id': t[1],
            'r2_id': t[2],
            'transloc_stat': t[3],
            'transloc_side': t[4],
            'sam_id': tt[0],
            'source': tt[1],
        })

    def trim(self, fastq_fpn, fastq_trimmed_fpn, umi_len):
        trim_params = {
            'read_struct': 'umi_1',
            'umi_1': {
                'len': umi_len,
            },
            'fastq': {
                'fpn': fastq_fpn + '.fastq.gz',
                'trimmed_fpn': fastq_trimmed_fpn + '.fastq.gz',
            },
        }
        umitrim_parser = umitrim(trim_params)
        df = umitrim_parser.todf()
        umitrim_parser.togz(df)
        return 0


if __name__ == "__main__":
    p = umiTranslocSelf(
        # metric='pcr_nums',
        # metric='pcr_errs',
        metric='seq_errs',
        # metric='ampl_rates',
        # metric='umi_lens',

        # method='unique',
        # method='cluster',
        # method='adjacency',
        # method='directional',
        # method='mcl',
        method='mcl_val',
        # method='mcl_ed',

        is_dedup=False,
        is_self_healing=True,
        umi_lib_fpn=to('data/simu/transloc/trimer/single_read/pcr8/'),
        fastq_fp=to('data/simu/transloc/trimer/single_read/pcr8/'),

    )
