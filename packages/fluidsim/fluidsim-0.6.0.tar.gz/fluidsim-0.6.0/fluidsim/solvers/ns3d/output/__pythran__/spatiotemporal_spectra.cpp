#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/include/builtins/abs.hpp>
#include <pythonic/include/builtins/enumerate.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/round.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/ge.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/abs.hpp>
#include <pythonic/builtins/enumerate.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/round.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/ge.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_spatiotemporal_spectra
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type0>())) __type1;
      typedef typename pythonic::returnable<__type1>::type __type2;
      typedef __type2 result_type;
    }  ;
    inline
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_spectrum_kzkhomega
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type1>::type>::type __type2;
      typedef __type2 __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type4;
      typedef __type4 __type5;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type5>::type>::type __type6;
      typedef __type6 __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type10;
      typedef std::integral_constant<long,1> __type11;
      typedef indexable_container<__type11, typename std::remove_reference<__type6>::type> __type12;
      typedef typename __combined<__type4,__type12>::type __type13;
      typedef __type13 __type14;
      typedef decltype(std::declval<__type10>()(std::declval<__type14>())) __type15;
      typedef typename pythonic::assignable<__type15>::type __type16;
      typedef __type16 __type17;
      typedef indexable_container<__type11, typename std::remove_reference<__type2>::type> __type18;
      typedef typename __combined<__type0,__type18>::type __type19;
      typedef __type19 __type20;
      typedef decltype(std::declval<__type10>()(std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<__type21>::type __type22;
      typedef __type22 __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type24;
      typedef __type24 __type25;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type25>())) __type26;
      typedef typename std::tuple_element<3,typename std::remove_reference<__type26>::type>::type __type27;
      typedef typename pythonic::assignable<__type27>::type __type28;
      typedef __type28 __type29;
      typedef long __type30;
      typedef decltype(pythonic::operator_::add(std::declval<__type29>(), std::declval<__type30>())) __type31;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type31>(), std::declval<__type30>())) __type32;
      typedef typename pythonic::assignable<__type32>::type __type33;
      typedef __type33 __type34;
      typedef decltype(std::declval<__type9>()(std::declval<__type17>(), std::declval<__type23>(), std::declval<__type34>())) __type35;
      typedef decltype(std::declval<__type8>()(std::declval<__type35>())) __type36;
      typedef typename pythonic::assignable<__type36>::type __type37;
      typedef decltype(std::declval<__type9>()(std::declval<__type17>(), std::declval<__type23>(), std::declval<__type29>())) __type41;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type25>())) __type43;
      typedef decltype(std::declval<__type8>()(std::declval<__type41>(), std::declval<__type43>())) __type44;
      typedef typename pythonic::assignable<__type44>::type __type45;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type46;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type47;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type48;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type49;
      typedef __type49 __type50;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type51;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type26>::type>::type __type52;
      typedef typename pythonic::lazy<__type52>::type __type53;
      typedef __type53 __type54;
      typedef decltype(std::declval<__type51>()(std::declval<__type54>())) __type55;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type55>::type::iterator>::value_type>::type __type56;
      typedef __type56 __type57;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type26>::type>::type __type58;
      typedef typename pythonic::lazy<__type58>::type __type59;
      typedef __type59 __type60;
      typedef decltype(std::declval<__type51>()(std::declval<__type60>())) __type61;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type61>::type::iterator>::value_type>::type __type62;
      typedef __type62 __type63;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type26>::type>::type __type64;
      typedef typename pythonic::lazy<__type64>::type __type65;
      typedef __type65 __type66;
      typedef decltype(std::declval<__type51>()(std::declval<__type66>())) __type67;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type67>::type::iterator>::value_type>::type __type68;
      typedef __type68 __type69;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type57>(), std::declval<__type63>(), std::declval<__type69>())) __type70;
      typedef decltype(std::declval<__type50>()[std::declval<__type70>()]) __type71;
      typedef decltype(std::declval<__type48>()(std::declval<__type71>())) __type72;
      typedef typename pythonic::assignable<__type6>::type __type73;
      typedef __type73 __type74;
      typedef decltype(pythonic::operator_::div(std::declval<__type72>(), std::declval<__type74>())) __type75;
      typedef decltype(std::declval<__type47>()(std::declval<__type75>())) __type76;
      typedef decltype(std::declval<__type46>()(std::declval<__type76>())) __type77;
      typedef typename pythonic::lazy<__type77>::type __type78;
      typedef decltype(pythonic::operator_::sub(std::declval<__type17>(), std::declval<__type30>())) __type80;
      typedef typename pythonic::lazy<__type80>::type __type81;
      typedef typename __combined<__type78,__type81>::type __type82;
      typedef __type82 __type83;
      typedef decltype(pythonic::operator_::sub(std::declval<__type23>(), std::declval<__type30>())) __type85;
      typedef typename pythonic::lazy<__type85>::type __type86;
      typedef __type86 __type87;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type88;
      typedef pythonic::types::contiguous_slice __type93;
      typedef decltype(std::declval<__type25>()(std::declval<__type57>(), std::declval<__type63>(), std::declval<__type69>(), std::declval<__type93>())) __type94;
      typedef typename pythonic::lazy<__type94>::type __type95;
      typedef __type95 __type96;
      typedef decltype(pythonic::operator_::mul(std::declval<__type30>(), std::declval<__type96>())) __type97;
      typedef typename pythonic::lazy<__type97>::type __type98;
      typedef typename __combined<__type95,__type98>::type __type99;
      typedef __type99 __type100;
      typedef decltype(std::declval<__type88>()(std::declval<__type100>())) __type101;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type101>::type::iterator>::value_type>::type __type102;
      typedef __type102 __type103;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type103>::type>::type __type104;
      typedef typename pythonic::lazy<__type104>::type __type105;
      typedef __type105 __type106;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type83>(), std::declval<__type87>(), std::declval<__type106>())) __type107;
      typedef indexable<__type107> __type108;
      typedef typename __combined<__type45,__type108>::type __type109;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type111;
      typedef __type111 __type112;
      typedef decltype(std::declval<__type112>()[std::declval<__type70>()]) __type117;
      typedef typename pythonic::assignable<__type117>::type __type118;
      typedef __type118 __type119;
      typedef typename pythonic::assignable<__type2>::type __type120;
      typedef __type120 __type121;
      typedef decltype(pythonic::operator_::div(std::declval<__type119>(), std::declval<__type121>())) __type122;
      typedef decltype(std::declval<__type46>()(std::declval<__type122>())) __type123;
      typedef typename pythonic::assignable<__type123>::type __type124;
      typedef __type124 __type125;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type83>(), std::declval<__type125>(), std::declval<__type106>())) __type133;
      typedef indexable<__type133> __type134;
      typedef typename __combined<__type109,__type134>::type __type135;
      typedef decltype(pythonic::operator_::add(std::declval<__type125>(), std::declval<__type30>())) __type138;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type83>(), std::declval<__type138>(), std::declval<__type106>())) __type140;
      typedef indexable<__type140> __type141;
      typedef typename __combined<__type135,__type141>::type __type142;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type103>::type>::type __type144;
      typedef typename pythonic::lazy<__type144>::type __type145;
      typedef __type145 __type146;
      typedef container<typename std::remove_reference<__type146>::type> __type147;
      typedef decltype(std::declval<__type20>()[std::declval<__type125>()]) __type151;
      typedef decltype(pythonic::operator_::sub(std::declval<__type119>(), std::declval<__type151>())) __type152;
      typedef decltype(pythonic::operator_::div(std::declval<__type152>(), std::declval<__type121>())) __type154;
      typedef typename pythonic::assignable<__type154>::type __type155;
      typedef __type155 __type156;
      typedef decltype(pythonic::operator_::sub(std::declval<__type30>(), std::declval<__type156>())) __type157;
      typedef typename pythonic::assignable<__type144>::type __type160;
      typedef __type160 __type161;
      typedef decltype(pythonic::operator_::mul(std::declval<__type157>(), std::declval<__type161>())) __type162;
      typedef container<typename std::remove_reference<__type162>::type> __type163;
      typedef decltype(pythonic::operator_::mul(std::declval<__type156>(), std::declval<__type161>())) __type166;
      typedef container<typename std::remove_reference<__type166>::type> __type167;
      typedef typename __combined<__type142,__type108,__type147,__type147,__type134,__type163,__type163,__type141,__type167,__type167>::type __type168;
      typedef __type168 __type169;
      typedef decltype(std::declval<__type169>()(std::declval<__type93>(), std::declval<__type93>(), std::declval<__type30>())) __type170;
      typedef container<typename std::remove_reference<__type170>::type> __type171;
      typedef decltype(std::declval<__type169>()(std::declval<__type93>(), std::declval<__type93>(), std::declval<__type93>())) __type173;
      typedef pythonic::types::slice __type175;
      typedef decltype(std::declval<__type169>()(std::declval<__type93>(), std::declval<__type93>(), std::declval<__type175>())) __type176;
      typedef decltype(pythonic::operator_::add(std::declval<__type173>(), std::declval<__type176>())) __type177;
      typedef container<typename std::remove_reference<__type177>::type> __type178;
      typedef typename __combined<__type37,__type171,__type178>::type __type179;
      typedef __type179 __type180;
      typedef decltype(pythonic::operator_::mul(std::declval<__type74>(), std::declval<__type121>())) __type183;
      typedef decltype(pythonic::operator_::div(std::declval<__type180>(), std::declval<__type183>())) __type184;
      typedef typename pythonic::returnable<__type184>::type __type185;
      typedef __type3 __ptype0;
      typedef __type7 __ptype1;
      typedef __type185 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& field_k0k1k2omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
    ;
  }  ;
  inline
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.12"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  inline
  typename compute_spectrum_kzkhomega::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type compute_spectrum_kzkhomega::operator()(argument_type0&& field_k0k1k2omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
    typedef std::integral_constant<long,1> __type4;
    typedef __type3 __type5;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type5>::type>::type __type6;
    typedef indexable_container<__type4, typename std::remove_reference<__type6>::type> __type7;
    typedef typename __combined<__type3,__type7>::type __type8;
    typedef __type8 __type9;
    typedef decltype(std::declval<__type2>()(std::declval<__type9>())) __type10;
    typedef typename pythonic::assignable<__type10>::type __type11;
    typedef __type11 __type12;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type13;
    typedef __type13 __type14;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type14>::type>::type __type15;
    typedef indexable_container<__type4, typename std::remove_reference<__type15>::type> __type16;
    typedef typename __combined<__type13,__type16>::type __type17;
    typedef __type17 __type18;
    typedef decltype(std::declval<__type2>()(std::declval<__type18>())) __type19;
    typedef typename pythonic::assignable<__type19>::type __type20;
    typedef __type20 __type21;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type22;
    typedef __type22 __type23;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type23>())) __type24;
    typedef typename std::tuple_element<3,typename std::remove_reference<__type24>::type>::type __type25;
    typedef typename pythonic::assignable<__type25>::type __type26;
    typedef __type26 __type27;
    typedef decltype(std::declval<__type1>()(std::declval<__type12>(), std::declval<__type21>(), std::declval<__type27>())) __type28;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type23>())) __type30;
    typedef decltype(std::declval<__type0>()(std::declval<__type28>(), std::declval<__type30>())) __type31;
    typedef typename pythonic::assignable<__type31>::type __type32;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type33;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type34;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type36;
    typedef __type36 __type37;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type38;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type24>::type>::type __type39;
    typedef typename pythonic::lazy<__type39>::type __type40;
    typedef __type40 __type41;
    typedef decltype(std::declval<__type38>()(std::declval<__type41>())) __type42;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type42>::type::iterator>::value_type>::type __type43;
    typedef __type43 __type44;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type24>::type>::type __type45;
    typedef typename pythonic::lazy<__type45>::type __type46;
    typedef __type46 __type47;
    typedef decltype(std::declval<__type38>()(std::declval<__type47>())) __type48;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type48>::type::iterator>::value_type>::type __type49;
    typedef __type49 __type50;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type24>::type>::type __type51;
    typedef typename pythonic::lazy<__type51>::type __type52;
    typedef __type52 __type53;
    typedef decltype(std::declval<__type38>()(std::declval<__type53>())) __type54;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type54>::type::iterator>::value_type>::type __type55;
    typedef __type55 __type56;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type44>(), std::declval<__type50>(), std::declval<__type56>())) __type57;
    typedef decltype(std::declval<__type37>()[std::declval<__type57>()]) __type58;
    typedef decltype(std::declval<__type35>()(std::declval<__type58>())) __type59;
    typedef typename pythonic::assignable<__type6>::type __type60;
    typedef __type60 __type61;
    typedef decltype(pythonic::operator_::div(std::declval<__type59>(), std::declval<__type61>())) __type62;
    typedef decltype(std::declval<__type34>()(std::declval<__type62>())) __type63;
    typedef decltype(std::declval<__type33>()(std::declval<__type63>())) __type64;
    typedef typename pythonic::lazy<__type64>::type __type65;
    typedef long __type67;
    typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type67>())) __type68;
    typedef typename pythonic::lazy<__type68>::type __type69;
    typedef typename __combined<__type65,__type69>::type __type70;
    typedef __type70 __type71;
    typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type67>())) __type73;
    typedef typename pythonic::lazy<__type73>::type __type74;
    typedef __type74 __type75;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type76;
    typedef pythonic::types::contiguous_slice __type81;
    typedef decltype(std::declval<__type23>()(std::declval<__type44>(), std::declval<__type50>(), std::declval<__type56>(), std::declval<__type81>())) __type82;
    typedef typename pythonic::lazy<__type82>::type __type83;
    typedef __type83 __type84;
    typedef decltype(pythonic::operator_::mul(std::declval<__type67>(), std::declval<__type84>())) __type85;
    typedef typename pythonic::lazy<__type85>::type __type86;
    typedef typename __combined<__type83,__type86>::type __type87;
    typedef __type87 __type88;
    typedef decltype(std::declval<__type76>()(std::declval<__type88>())) __type89;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type89>::type::iterator>::value_type>::type __type90;
    typedef __type90 __type91;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type91>::type>::type __type92;
    typedef typename pythonic::lazy<__type92>::type __type93;
    typedef __type93 __type94;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type71>(), std::declval<__type75>(), std::declval<__type94>())) __type95;
    typedef indexable<__type95> __type96;
    typedef typename __combined<__type32,__type96>::type __type97;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type99;
    typedef __type99 __type100;
    typedef decltype(std::declval<__type100>()[std::declval<__type57>()]) __type105;
    typedef typename pythonic::assignable<__type105>::type __type106;
    typedef __type106 __type107;
    typedef typename pythonic::assignable<__type15>::type __type108;
    typedef __type108 __type109;
    typedef decltype(pythonic::operator_::div(std::declval<__type107>(), std::declval<__type109>())) __type110;
    typedef decltype(std::declval<__type33>()(std::declval<__type110>())) __type111;
    typedef typename pythonic::assignable<__type111>::type __type112;
    typedef __type112 __type113;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type71>(), std::declval<__type113>(), std::declval<__type94>())) __type121;
    typedef indexable<__type121> __type122;
    typedef typename __combined<__type97,__type122>::type __type123;
    typedef decltype(pythonic::operator_::add(std::declval<__type113>(), std::declval<__type67>())) __type126;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type71>(), std::declval<__type126>(), std::declval<__type94>())) __type128;
    typedef indexable<__type128> __type129;
    typedef typename __combined<__type123,__type129>::type __type130;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type91>::type>::type __type132;
    typedef typename pythonic::lazy<__type132>::type __type133;
    typedef __type133 __type134;
    typedef container<typename std::remove_reference<__type134>::type> __type135;
    typedef decltype(std::declval<__type18>()[std::declval<__type113>()]) __type139;
    typedef decltype(pythonic::operator_::sub(std::declval<__type107>(), std::declval<__type139>())) __type140;
    typedef decltype(pythonic::operator_::div(std::declval<__type140>(), std::declval<__type109>())) __type142;
    typedef typename pythonic::assignable<__type142>::type __type143;
    typedef __type143 __type144;
    typedef decltype(pythonic::operator_::sub(std::declval<__type67>(), std::declval<__type144>())) __type145;
    typedef typename pythonic::assignable<__type132>::type __type148;
    typedef __type148 __type149;
    typedef decltype(pythonic::operator_::mul(std::declval<__type145>(), std::declval<__type149>())) __type150;
    typedef container<typename std::remove_reference<__type150>::type> __type151;
    typedef decltype(pythonic::operator_::mul(std::declval<__type144>(), std::declval<__type149>())) __type154;
    typedef container<typename std::remove_reference<__type154>::type> __type155;
    typedef typename __combined<__type130,__type96,__type135,__type122,__type151,__type129,__type155>::type __type156;
    typedef typename pythonic::assignable<__type156>::type __type157;
    typedef typename pythonic::lazy<__type87>::type __type158;
    typedef typename pythonic::lazy<__type70>::type __type159;
    typedef typename pythonic::assignable<__type143>::type __type160;
    typedef decltype(pythonic::operator_::add(std::declval<__type27>(), std::declval<__type67>())) __type164;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type164>(), std::declval<__type67>())) __type165;
    typedef typename pythonic::assignable<__type165>::type __type166;
    typedef __type166 __type167;
    typedef decltype(std::declval<__type1>()(std::declval<__type12>(), std::declval<__type21>(), std::declval<__type167>())) __type168;
    typedef decltype(std::declval<__type0>()(std::declval<__type168>())) __type169;
    typedef typename pythonic::assignable<__type169>::type __type170;
    typedef __type156 __type171;
    typedef decltype(std::declval<__type171>()(std::declval<__type81>(), std::declval<__type81>(), std::declval<__type67>())) __type172;
    typedef container<typename std::remove_reference<__type172>::type> __type173;
    typedef decltype(std::declval<__type171>()(std::declval<__type81>(), std::declval<__type81>(), std::declval<__type81>())) __type175;
    typedef pythonic::types::slice __type177;
    typedef decltype(std::declval<__type171>()(std::declval<__type81>(), std::declval<__type81>(), std::declval<__type177>())) __type178;
    typedef decltype(pythonic::operator_::add(std::declval<__type175>(), std::declval<__type178>())) __type179;
    typedef container<typename std::remove_reference<__type179>::type> __type180;
    typedef typename __combined<__type170,__type173,__type180>::type __type181;
    typedef typename pythonic::assignable<__type181>::type __type182;
    typename pythonic::assignable_noescape<decltype(std::get<1>(khs))>::type deltakh = std::get<1>(khs);
    typename pythonic::assignable_noescape<decltype(std::get<1>(kzs))>::type deltakz = std::get<1>(kzs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(khs))>::type nkh = pythonic::builtins::functor::len{}(khs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(kzs))>::type nkz = pythonic::builtins::functor::len{}(kzs);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega)))>::type nk0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega)))>::type nk1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega)))>::type nk2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega));
    typename pythonic::assignable_noescape<decltype(std::get<3>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega)))>::type nomega = std::get<3>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1k2omega));
    __type157 spectrum_kzkhomega = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega), pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, field_k0k1k2omega));
    {
      long  __target139708405892480 = nk0;
      for (long  ik0=0L; ik0 < __target139708405892480; ik0 += 1L)
      {
        {
          long  __target139708406014976 = nk1;
          for (long  ik1=0L; ik1 < __target139708406014976; ik1 += 1L)
          {
            {
              long  __target139708406015600 = nk2;
              for (long  ik2=0L; ik2 < __target139708406015600; ik2 += 1L)
              {
                __type158 values = field_k0k1k2omega(ik0,ik1,ik2,pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None));
                if (pythonic::operator_::ne(KX[pythonic::types::make_tuple(ik0, ik1, ik2)], 0.0))
                {
                  values = pythonic::operator_::mul(2L, values);
                }
                typename pythonic::assignable_noescape<decltype(KH[pythonic::types::make_tuple(ik0, ik1, ik2)])>::type kappa = KH[pythonic::types::make_tuple(ik0, ik1, ik2)];
                typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh)))>::type ikh = pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh));
                __type159 ikz = pythonic::builtins::functor::int_{}(pythonic::builtins::functor::round{}(pythonic::operator_::div(pythonic::builtins::functor::abs{}(KZ[pythonic::types::make_tuple(ik0, ik1, ik2)]), deltakz)));
                if (pythonic::operator_::ge(ikz, pythonic::operator_::sub(nkz, 1L)))
                {
                  ikz = pythonic::operator_::sub(nkz, 1L);
                }
                {
                  __type160 coef_share;
                  if (pythonic::operator_::ge(ikh, pythonic::operator_::sub(nkh, 1L)))
                  {
                    typename pythonic::lazy<decltype(pythonic::operator_::sub(nkh, 1L))>::type ikh_ = pythonic::operator_::sub(nkh, 1L);
                    {
                      for (auto&& __tuple0: pythonic::builtins::functor::enumerate{}(values))
                      {
                        typename pythonic::lazy<decltype(std::get<1>(__tuple0))>::type value = std::get<1>(__tuple0);
                        typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type i = std::get<0>(__tuple0);
                        spectrum_kzkhomega[pythonic::types::make_tuple(ikz, ikh_, i)] += value;
                      }
                    }
                  }
                  else
                  {
                    coef_share = pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh);
                    {
                      for (auto&& __tuple1: pythonic::builtins::functor::enumerate{}(values))
                      {
                        typename pythonic::assignable_noescape<decltype(std::get<1>(__tuple1))>::type value_ = std::get<1>(__tuple1);
                        typename pythonic::lazy<decltype(std::get<0>(__tuple1))>::type i_ = std::get<0>(__tuple1);
                        spectrum_kzkhomega[pythonic::types::make_tuple(ikz, ikh, i_)] += pythonic::operator_::mul(pythonic::operator_::sub(1L, coef_share), value_);
                        spectrum_kzkhomega[pythonic::types::make_tuple(ikz, pythonic::operator_::add(ikh, 1L), i_)] += pythonic::operator_::mul(coef_share, value_);
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L))>::type nomega_ = pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L);
    __type182 spectrum_onesided = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega_));
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L) = spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L);
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(1L,pythonic::builtins::None)) = pythonic::operator_::add(spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(1L,nomega_)), spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::slice(-1L,pythonic::operator_::neg(nomega_),-1L)));
    return pythonic::operator_::div(spectrum_onesided, pythonic::operator_::mul(deltakz, deltakh));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_spatiotemporal_spectra::__transonic__()());
inline
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type compute_spectrum_kzkhomega0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long,long>>&& field_k0k1k2omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1k2omega, khs, kzs, KX, KZ, KH);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type compute_spectrum_kzkhomega1(pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long,long>>&& field_k0k1k2omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1k2omega, khs, kzs, KX, KZ, KH);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_spectrum_kzkhomega0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"field_k0k1k2omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_spectrum_kzkhomega1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"field_k0k1k2omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega1(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_spectrum_kzkhomega(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_spectrum_kzkhomega0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_spectrum_kzkhomega1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_spectrum_kzkhomega", "\n""    - compute_spectrum_kzkhomega(float64[:,:,:,:], float64[:], float64[:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:,:], float64[:], float64[:], float64[:,:,:], float64[:,:,:], float64[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_spectrum_kzkhomega",
    (PyCFunction)__pythran_wrapall_compute_spectrum_kzkhomega,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the kz-kh-omega spectrum.\n""\n""    Supported prototypes:\n""\n""    - compute_spectrum_kzkhomega(float64[:,:,:,:], float64[:], float64[:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:,:], float64[:], float64[:], float64[:,:,:], float64[:,:,:], float64[:,:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "spatiotemporal_spectra",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(spatiotemporal_spectra)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(spatiotemporal_spectra)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("spatiotemporal_spectra",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-02-04 12:30:20.760785",
                                      "2a66b801204fdcf6d6794faccf6158a29fd4f733293ee1c8d7abf074f174afb6");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif