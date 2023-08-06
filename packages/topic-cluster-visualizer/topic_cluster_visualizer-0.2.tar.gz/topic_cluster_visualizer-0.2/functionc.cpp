// [[Rcpp::depends(RcppArmadillo)]]
// [[Rcpp::depends(RcppArmadillo)]]

#pragma warning(disable: 4819)



#ifdef _DEBUG
#define _DEBUG_WAS_DEFINED 1
#undef _DEBUG
#endif

#include "Python.h"

#ifdef _DEBUG_WAS_DEFINED
#define _DEBUG 1
#undef _DEBUG_WAS_DEFINED
#endif

#include <vector>
#include <chrono>
#include <iostream>

/*
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
*/

#include "carma"

#include <armadillo>

#include "functionc.hpp"

// #include <windows.h>
#include <stdio.h>


namespace py = pybind11;

using namespace std;
using namespace arma;



void DoProgress( int progress, int total )
{
    int barLength = 72;
	int pos = progress * barLength / total;

	std::cout << "Iteration: [";
	for(int i=0; i != barLength; ++i)
	{
		if(i < pos)
			std::cout << "#";
		else
			std::cout << " ";
	}
	std::cout << "]" << progress << "/" << total << "\r";
}





std::vector<py::array_t<double>>
onepl_lsrm_cont_missing
(
    arma::Mat<double> input,

    const int ndim,
    const int niter,
    const int nburn,
    const int nthin,
    const int nprint,

    const double jump_beta,
    const double jump_theta,
    const double jump_gamma,
    const double jump_z,
    const double jump_w,

    const double pr_mean_beta,
    const double pr_sd_beta,
    const double pr_a_th_sigma,
    const double pr_b_th_sigma,
    const double pr_mean_theta,
    const double pr_a_sigma,
    const double pr_b_sigma,
    const double pr_mean_gamma,
    const double pr_sd_gamma,

    const double missing
)
{

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    arma::Mat<double> data = input;

    

    const int nsample = int(data.n_rows);
    const int nitem = int(data.n_cols);

    int i, j, k, count, accept;
    double num, den, old_like_beta, new_like_beta, old_like_theta, new_like_theta;
    double old_like_z, new_like_z, old_like_w, new_like_w, old_like_gamma, new_like_gamma;
    double ratio, un, dist_temp, dist_old_temp, dist_new_temp;
    double post_a_sigma, post_b_sigma, post_a_th_sigma, post_b_th_sigma;
    double pr_mean_z = 0.0, pr_sd_z = 1.0, pr_mean_w = 0.0, pr_sd_w = 1.0, pr_sd = 1.0, pr_sd_theta = 1.0, mle;


    dvec oldbeta(nitem, fill::randu);
    oldbeta = oldbeta * 4.0 - 2.0;
    dvec newbeta = oldbeta;

    dvec oldtheta(nsample, fill::randu);
    oldtheta = oldtheta * 4.0 - 2.0;
    dvec newtheta = oldtheta;

    dmat oldz(nsample, ndim, fill::randu);
    oldz = oldz * 2.0 - 1.0;
    dmat newz = oldz;

    dmat oldw(nitem, ndim, fill::randu);
    oldw = oldw * 2.0 - 1.0;
    dmat neww = oldw;

    double oldgamma = 1, newgamma = 1; //gamma = log(gamma)
    dmat samp_beta((niter - nburn) / nthin, nitem, fill::zeros);
    dmat samp_theta((niter - nburn) / nthin, nsample, fill::zeros);
    dcube samp_z(((niter - nburn) / nthin), nsample, ndim, fill::zeros);
    dcube samp_w(((niter - nburn) / nthin), nitem, ndim, fill::zeros);
    dvec samp_sd_theta((niter - nburn) / nthin, fill::zeros);
    dvec samp_sd((niter - nburn) / nthin, fill::zeros);
    dvec samp_mle((niter - nburn) / nthin, fill::zeros);
    dvec samp_gamma(((niter - nburn) / nthin), fill::zeros);

    dvec accept_beta(nitem, fill::zeros);
    dvec accept_theta(nsample, fill::zeros);
    dvec accept_z(nsample, fill::zeros);
    dvec accept_w(nitem, fill::zeros);
    double accept_gamma = 0;

    accept = count = 0;

    dmat dist(nsample, nitem, fill::zeros);
    dvec old_dist_k(nitem, fill::zeros);
    dvec new_dist_k(nitem, fill::zeros);
    dvec old_dist_i(nsample, fill::zeros);
    dvec new_dist_i(nsample, fill::zeros);
	
    for (int iter = 0; iter < niter; iter++) 
    {
 
        DoProgress( iter, niter );
		
		//dist(j,i) is distance of z_j and w_i
        dist.fill(0.0);
        for (i = 0; i < nitem; i++) 
        {
            for (k = 0; k < nsample; k++) 
            {
                dist_temp = 0.0;
                for (j = 0; j < ndim; j++) dist_temp += pow((oldz(k, j) - oldw(i, j)), 2.0);
                dist(k, i) = sqrt(dist_temp);
            }
        }

        // beta update
        for (i = 0; i < nitem; i++)
        {
            newbeta(i) = oldbeta(i) + jump_beta * randn();
            // newbeta(i) = R::rnorm(oldbeta(i), jump_beta);
            old_like_beta = new_like_beta = 0.0;
            for (k = 0; k < nsample; k++)
            {
                if (data(k, i) != missing)
                {
                    new_like_beta += -pow((data(k, i) - newbeta(i) - oldtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                    old_like_beta += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                }
            }

            num = new_like_beta + log_normpdf(newbeta(i), pr_mean_beta, pr_sd_beta);
            den = old_like_beta + log_normpdf(oldbeta(i), pr_mean_beta, pr_sd_beta);
            ratio = num - den;

            if (ratio > 0.0) accept = 1;
            else
            {
                un = randu();
                if (log(un) < ratio) accept = 1;
                else accept = 0;
            }

            if (accept == 1)
            {
                oldbeta(i) = newbeta(i);
                accept_beta(i) += 1.0 / (niter * 1.0);
            }
            else newbeta(i) = oldbeta(i);

        }

        // theta update
        for (k = 0; k < nsample; k++)
        {
            newtheta(k) = oldtheta(k) + jump_theta * randn();
            old_like_theta = new_like_theta = 0.0;

            for (i = 0; i < nitem; i++)
            {
                if (data(k, i) != missing)
                {
                    new_like_theta += -pow((data(k, i) - oldbeta(i) - newtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                    old_like_theta += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                }
            }
            num = new_like_theta + log_normpdf(newtheta(k), pr_mean_theta, pr_sd_theta);
            den = old_like_theta + log_normpdf(oldtheta(k), pr_mean_theta, pr_sd_theta);
            ratio = num - den;

            if (ratio > 0.0) accept = 1;
            else
            {
                un = randu();
                if (log(un) < ratio) accept = 1;
                else accept = 0;
            }

            if (accept == 1)
            {
                oldtheta(k) = newtheta(k);
                accept_theta(k) += 1.0 / (niter * 1.0);
            }
            else newtheta(k) = oldtheta(k);
        }

        // gamma(log(gamma)) update
        newgamma = exp(log(oldgamma) + jump_gamma * randn());
        old_like_gamma = 0.0;
        new_like_gamma = 0.0;

        for (k = 0; k < nsample; k++)
        {
            for (i = 0; i < nitem; i++)
            {
                if (data(k, i) != missing)
                {
                    new_like_gamma += -pow((data(k, i) - oldbeta(i) - newtheta(k) + newgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                    old_like_gamma += -pow((data(k, i) - oldbeta(i) - newtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                }
            }
        }


        num = new_like_gamma +
            log_normpdf(log(oldgamma), log(newgamma), jump_gamma) +
            log_normpdf(log(newgamma), pr_mean_gamma, pr_sd_gamma);
        //R::dlnorm(oldgamma, std::log(newgamma), jump_gamma, 1) + 
        //R::dlnorm(newgamma, pr_mean_gamma, pr_sd_gamma, 1);
        den = old_like_gamma +
            log_normpdf(log(newgamma), log(oldgamma), jump_gamma) +
            log_normpdf(log(oldgamma), pr_mean_gamma, pr_sd_gamma);
        //R::dlnorm(newgamma, std::log(oldgamma), jump_gamma, 1) + 
        //R::dlnorm(oldgamma, pr_mean_gamma, pr_sd_gamma, 1);
        ratio = num - den;

        if (ratio > 0.0) accept = 1;
        else
        {
            un = randu();
            if (log(un) < ratio) accept = 1;
            else accept = 0;
        }

        if (accept == 1)
        {
            oldgamma = newgamma;
            accept_gamma += 1.0 / (niter * 1.0);
        }
        else newgamma = oldgamma;

        // zj update
        for (k = 0; k < nsample; k++)
        {
            for (j = 0; j < ndim; j++) newz(k, j) = oldz(k, j) + jump_z * randn();
            old_like_z = new_like_z = 0.0;

            //calculate distance of oldw and newz
            for (i = 0; i < nitem; i++)
            {
                dist_old_temp = dist_new_temp = 0.0;
                for (j = 0; j < ndim; j++)
                {
                    dist_new_temp += pow((newz(k, j) - oldw(i, j)), 2.0);
                    dist_old_temp += pow((oldz(k, j) - oldw(i, j)), 2.0);
                }
                new_dist_k(i) = sqrt(dist_new_temp);
                old_dist_k(i) = sqrt(dist_old_temp);
            }

            //calculate likelihood
            for (i = 0; i < nitem; i++)
            {
                if (data(k, i) != missing)
                {
                    new_like_z += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * new_dist_k(i)), 2) / (2 * pow(pr_sd, 2));
                    old_like_z += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * old_dist_k(i)), 2) / (2 * pow(pr_sd, 2));
                }
            }

            num = den = 0.0;
            for (j = 0; j < ndim; j++)
            {
                num += log_normpdf(newz(k, j), pr_mean_z, pr_sd_z);
                //#num += scipy.stats.norm.logpdf(newz[k, j], pr_mean_z, pr_sd_z)
                den += log_normpdf(oldz(k, j), pr_mean_z, pr_sd_z);
            }
            //Rprintf("%.3f %.3f %.3f %.3f\n", num, den, new_like_z, old_like_z);
            //arma::dvec newzz = dmvnorm(newz.cols(2*j,2*j+1),pr_mean_z,pr_cov_z,TRUE);
            //arma::dvec oldzz = dmvnorm(oldz.cols(2*j,2*j+1),pr_mean_z,pr_cov_z,TRUE);

            num += new_like_z;
            den += old_like_z;
            ratio = num - den;

            if (ratio > 0.0) accept = 1;
            else
            {
                un = randu();
                if (log(un) < ratio) accept = 1;
                else accept = 0;
            }

            if (accept == 1)
            {
                for (j = 0; j < ndim; j++) oldz(k, j) = newz(k, j);
                accept_z(k) += 1.0 / (niter * 1.0);
            }
            else
            {
                for (j = 0; j < ndim; j++) newz(k, j) = oldz(k, j);
            }
        }

        // wi update
        for (i = 0; i < nitem; i++) 
        {
            for (j = 0; j < ndim; j++) neww(i, j) = oldw(i, j) + jump_w * randn();
            old_like_w = new_like_w = 0.0;

            //calculate distance of neww and oldz
            for (k = 0; k < nsample; k++) 
            {
                dist_old_temp = dist_new_temp = 0.0;
                for (j = 0; j < ndim; j++) 
                {
                    dist_new_temp += pow((oldz(k, j) - neww(i, j)), 2.0);
                    dist_old_temp += pow((oldz(k, j) - oldw(i, j)), 2.0);
                }
                new_dist_i(k) = sqrt(dist_new_temp);
                old_dist_i(k) = sqrt(dist_old_temp);
            }

            //calculate likelihood
            for (k = 0; k < nsample; k++) {
                if (data(k, i) != missing) {
                    new_like_w += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * new_dist_i(k)), 2) / (2 * pow(pr_sd, 2));
                    old_like_w += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * old_dist_i(k)), 2) / (2 * pow(pr_sd, 2));
                }
            }

            num = den = 0.0;
            for (j = 0; j < ndim; j++) {
                num += log_normpdf(neww(i, j), pr_mean_w, pr_sd_w);
                den += log_normpdf(oldw(i, j), pr_mean_w, pr_sd_w);
            }

            num += new_like_w;
            den += old_like_w;
            ratio = num - den;

            if (ratio > 0.0) accept = 1;
            else {
                un = randu();
                if (log(un) < ratio) accept = 1;
                else accept = 0;
            }

            if (accept == 1) {
                for (j = 0; j < ndim; j++) oldw(i, j) = neww(i, j);
                accept_w(i) += 1.0 / (niter * 1.0);
            }
            else {
                for (j = 0; j < ndim; j++) neww(i, j) = oldw(i, j);
            }
        }


        //sigma_theta update with gibbs
        post_a_th_sigma = 2 * pr_a_th_sigma + nsample;
        post_b_th_sigma = pr_b_th_sigma;
        for (j = 0; j < nsample; j++) post_b_th_sigma += pow((oldtheta(j) - pr_mean_theta), 2.0);
        pr_sd_theta = sqrt(2 * post_b_th_sigma * (1.0 / chi2rnd(post_a_th_sigma)));

        //dist(j,i) is distance of z_j and w_i
        dist.fill(0.0);
        for (i = 0; i < nitem; i++) {
            for (k = 0; k < nsample; k++) {
                dist_temp = 0.0;
                for (j = 0; j < ndim; j++) dist_temp += pow((oldz(k, j) - oldw(i, j)), 2.0);
                dist(k, i) = sqrt(dist_temp);
            }
        }


        //sigma update with gibbs
        post_a_sigma = 2 * pr_a_sigma + nsample * nitem;
        post_b_sigma = pr_b_sigma;
        for (j = 0; j < nsample; j++) {
            for (i = 0; i < nitem; i++) post_b_sigma += pow((data(j, i) - oldbeta(i) - oldtheta(j) + oldgamma * dist(j, i)), 2.0) / 2;
        }
        pr_sd = sqrt(2 * post_b_sigma * (1.0 / chi2rnd(post_a_th_sigma)));

        // burn, thin
        if (iter >= nburn && iter % nthin == 0) {
            for (i = 0; i < nitem; i++) samp_beta(count, i) = oldbeta(i);
            for (k = 0; k < nsample; k++) samp_theta(count, k) = oldtheta(k);
            for (i = 0; i < nitem; i++) {
                for (j = 0; j < ndim; j++) {
                    samp_w(count, i, j) = oldw(i, j);
                }
            }
            for (k = 0; k < nsample; k++) {
                for (j = 0; j < ndim; j++) {
                    samp_z(count, k, j) = oldz(k, j);
                }
            }

            samp_gamma(count) = oldgamma;
            samp_sd_theta(count) = pr_sd_theta;
            samp_sd(count) = pr_sd;

            mle = 0.0;
            for (i = 0; i < nitem; i++) mle += log_normpdf(oldbeta(i), pr_mean_beta, pr_sd_beta);
            for (k = 0; k < nsample; k++) mle += log_normpdf(oldtheta(k), pr_mean_theta, pr_sd_theta);
            for (i = 0; i < nitem; i++)
                for (j = 0; j < ndim; j++) mle += log_normpdf(oldw(i, j), pr_mean_w, pr_sd_w);
            for (k = 0; k < nsample; k++)
                for (j = 0; j < ndim; j++) mle += log_normpdf(oldz(k, j), pr_mean_z, pr_sd_z);
            for (k = 0; k < nsample; k++) {
                for (i = 0; i < nitem; i++) {
                    mle += -pow((data(k, i) - oldbeta(i) - oldtheta(k) + oldgamma * dist(k, i)), 2) / (2 * pow(pr_sd, 2));
                }
            }
            mle += log_normpdf(log(oldgamma), pr_mean_gamma, pr_sd_gamma);
            samp_mle(count) = mle;

            count++;
        }
		
		/*
        if (iter % nprint == 0)
        {
            printf("Iteration: %.5u ", iter);
            for (i = 0; i < nitem; i++)
            {
                printf("% .3f ", oldbeta(i));
            }
            printf(" %.3f ", oldgamma);
            printf(" %.3f\n", pr_sd_theta);
        }*/
		



    } //for end

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    //������ �Ƹ��� ������ �Է��ϰ� �з����� �����ϱ� ���������� ���ϵǴ°� Ȯ��
    //���� �����̸� �ְ� �̰� �Ƹ����� ��ȯ �� ���� �� �����̷� ��ȯ�ؼ� ����
    //�ش�������� ī���� �ʿ�
    //�� ���е��� ����Ʈ�� ��ҷ� ����ִ´�

    
    std::vector<py::array_t<double>> matrices;

    //������Ʈ���� cube�� ����

    matrices.push_back(carma::mat_to_arr(samp_beta, false));//FIXME:
    matrices.push_back(carma::mat_to_arr(samp_theta, false));//FIXME:
    matrices.push_back(carma::cube_to_arr(samp_z, false)); //FIXME:
    matrices.push_back(carma::cube_to_arr(samp_w, false)); //FIXME:
    matrices.push_back(carma::col_to_arr(samp_gamma, false));//FIXME:
    matrices.push_back(carma::col_to_arr(samp_sd_theta, false));//FIXME:
    matrices.push_back(carma::col_to_arr(samp_sd, false));
    matrices.push_back(carma::col_to_arr(samp_mle, false));
    matrices.push_back(carma::col_to_arr(accept_beta, false));
    matrices.push_back(carma::col_to_arr(accept_theta, false));
    matrices.push_back(carma::col_to_arr(accept_z, false));
    matrices.push_back(carma::col_to_arr(accept_w, false));
    
    //����Ʈ ��ҷ� �Ϸ��� ��̿��� �ؼ� ���Ʈ���� ������ ��� �ۼ�

    auto accept_gamma_arr = py::array_t<double>({ 1 });
    accept_gamma_arr.mutable_at(0) = accept_gamma;

    matrices.push_back(accept_gamma_arr);
    
    //cout �����۵���
    //����뿡�� ������ �𸣰ڴµ� arma ��Ʈ������ ���� ũ�� �̻��̸� ����� �ȵ�

    /*
    samp_beta.print("B");
    samp_theta.print("B");
    samp_z.print("B");
    samp_w.print("B");
    samp_gamma.print("B");
    samp_sd_theta.print("B");
    samp_sd.print("B");
    samp_mle.print("B");
    accept_beta.print("B");
    accept_theta.print("B");
    accept_z.print("B");
    accept_w.print("B");
    */

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout 
        << "Time difference (sec) = " 
        << (std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count()) / 1000000.0 
        << " seconds"
        << std::endl;

    return matrices;

    //return matrices;
} // function end

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*

py::array_t<double> return_results(arma::field<cube> input, int col)
{
    py::array_t<double> value{};

    if (col == 2 || 3 || 12)
        value = carma::cube_to_arr(input(0, col));

    else
        value = carma::mat_to_arr(input(0, col).slice(0));

    return value;

};

*/

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

PYBIND11_MODULE(functionc, m)
{
    m.doc() = "minimal working example";
    m.def("onepl_lsrm_cont_missing", &onepl_lsrm_cont_missing);
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
int main(int argc, char** argv)
{
    mat A(4, 3, fill::zeros);

    onepl_lsrm_cont_missing
    (
        A, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1
    ).print("A");

    return 0;


}
*/
