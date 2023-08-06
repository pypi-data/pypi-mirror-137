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
      typedef typename std::tuple_element<2,typename std::remove_reference<__type26>::type>::type __type27;
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
      typedef decltype(pythonic::types::make_tuple(std::declval<__type57>(), std::declval<__type63>())) __type64;
      typedef decltype(std::declval<__type50>()[std::declval<__type64>()]) __type65;
      typedef decltype(std::declval<__type48>()(std::declval<__type65>())) __type66;
      typedef typename pythonic::assignable<__type6>::type __type67;
      typedef __type67 __type68;
      typedef decltype(pythonic::operator_::div(std::declval<__type66>(), std::declval<__type68>())) __type69;
      typedef decltype(std::declval<__type47>()(std::declval<__type69>())) __type70;
      typedef decltype(std::declval<__type46>()(std::declval<__type70>())) __type71;
      typedef typename pythonic::lazy<__type71>::type __type72;
      typedef decltype(pythonic::operator_::sub(std::declval<__type17>(), std::declval<__type30>())) __type74;
      typedef typename pythonic::lazy<__type74>::type __type75;
      typedef typename __combined<__type72,__type75>::type __type76;
      typedef __type76 __type77;
      typedef decltype(pythonic::operator_::sub(std::declval<__type23>(), std::declval<__type30>())) __type79;
      typedef typename pythonic::lazy<__type79>::type __type80;
      typedef __type80 __type81;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type82;
      typedef pythonic::types::contiguous_slice __type86;
      typedef decltype(std::declval<__type25>()(std::declval<__type57>(), std::declval<__type63>(), std::declval<__type86>())) __type87;
      typedef typename pythonic::lazy<__type87>::type __type88;
      typedef __type88 __type89;
      typedef decltype(pythonic::operator_::mul(std::declval<__type30>(), std::declval<__type89>())) __type90;
      typedef typename pythonic::lazy<__type90>::type __type91;
      typedef typename __combined<__type88,__type91>::type __type92;
      typedef __type92 __type93;
      typedef decltype(std::declval<__type82>()(std::declval<__type93>())) __type94;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type94>::type::iterator>::value_type>::type __type95;
      typedef __type95 __type96;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type96>::type>::type __type97;
      typedef typename pythonic::lazy<__type97>::type __type98;
      typedef __type98 __type99;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type77>(), std::declval<__type81>(), std::declval<__type99>())) __type100;
      typedef indexable<__type100> __type101;
      typedef typename __combined<__type45,__type101>::type __type102;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type104;
      typedef __type104 __type105;
      typedef decltype(std::declval<__type105>()[std::declval<__type64>()]) __type109;
      typedef typename pythonic::assignable<__type109>::type __type110;
      typedef __type110 __type111;
      typedef typename pythonic::assignable<__type2>::type __type112;
      typedef __type112 __type113;
      typedef decltype(pythonic::operator_::div(std::declval<__type111>(), std::declval<__type113>())) __type114;
      typedef decltype(std::declval<__type46>()(std::declval<__type114>())) __type115;
      typedef typename pythonic::assignable<__type115>::type __type116;
      typedef __type116 __type117;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type77>(), std::declval<__type117>(), std::declval<__type99>())) __type125;
      typedef indexable<__type125> __type126;
      typedef typename __combined<__type102,__type126>::type __type127;
      typedef decltype(pythonic::operator_::add(std::declval<__type117>(), std::declval<__type30>())) __type130;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type77>(), std::declval<__type130>(), std::declval<__type99>())) __type132;
      typedef indexable<__type132> __type133;
      typedef typename __combined<__type127,__type133>::type __type134;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type96>::type>::type __type136;
      typedef typename pythonic::lazy<__type136>::type __type137;
      typedef __type137 __type138;
      typedef container<typename std::remove_reference<__type138>::type> __type139;
      typedef decltype(std::declval<__type20>()[std::declval<__type117>()]) __type143;
      typedef decltype(pythonic::operator_::sub(std::declval<__type111>(), std::declval<__type143>())) __type144;
      typedef decltype(pythonic::operator_::div(std::declval<__type144>(), std::declval<__type113>())) __type146;
      typedef typename pythonic::assignable<__type146>::type __type147;
      typedef __type147 __type148;
      typedef decltype(pythonic::operator_::sub(std::declval<__type30>(), std::declval<__type148>())) __type149;
      typedef typename pythonic::assignable<__type136>::type __type152;
      typedef __type152 __type153;
      typedef decltype(pythonic::operator_::mul(std::declval<__type149>(), std::declval<__type153>())) __type154;
      typedef container<typename std::remove_reference<__type154>::type> __type155;
      typedef decltype(pythonic::operator_::mul(std::declval<__type148>(), std::declval<__type153>())) __type158;
      typedef container<typename std::remove_reference<__type158>::type> __type159;
      typedef typename __combined<__type134,__type101,__type139,__type139,__type126,__type155,__type155,__type133,__type159,__type159>::type __type160;
      typedef __type160 __type161;
      typedef decltype(std::declval<__type161>()(std::declval<__type86>(), std::declval<__type86>(), std::declval<__type30>())) __type162;
      typedef container<typename std::remove_reference<__type162>::type> __type163;
      typedef decltype(std::declval<__type161>()(std::declval<__type86>(), std::declval<__type86>(), std::declval<__type86>())) __type165;
      typedef pythonic::types::slice __type167;
      typedef decltype(std::declval<__type161>()(std::declval<__type86>(), std::declval<__type86>(), std::declval<__type167>())) __type168;
      typedef decltype(pythonic::operator_::add(std::declval<__type165>(), std::declval<__type168>())) __type169;
      typedef container<typename std::remove_reference<__type169>::type> __type170;
      typedef typename __combined<__type37,__type163,__type170>::type __type171;
      typedef __type171 __type172;
      typedef decltype(pythonic::operator_::mul(std::declval<__type68>(), std::declval<__type113>())) __type175;
      typedef decltype(pythonic::operator_::div(std::declval<__type172>(), std::declval<__type175>())) __type176;
      typedef typename pythonic::returnable<__type176>::type __type177;
      typedef __type3 __ptype0;
      typedef __type7 __ptype1;
      typedef __type177 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& field_k0k1omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
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
  typename compute_spectrum_kzkhomega::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type compute_spectrum_kzkhomega::operator()(argument_type0&& field_k0k1omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
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
    typedef typename std::tuple_element<2,typename std::remove_reference<__type24>::type>::type __type25;
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
    typedef decltype(pythonic::types::make_tuple(std::declval<__type44>(), std::declval<__type50>())) __type51;
    typedef decltype(std::declval<__type37>()[std::declval<__type51>()]) __type52;
    typedef decltype(std::declval<__type35>()(std::declval<__type52>())) __type53;
    typedef typename pythonic::assignable<__type6>::type __type54;
    typedef __type54 __type55;
    typedef decltype(pythonic::operator_::div(std::declval<__type53>(), std::declval<__type55>())) __type56;
    typedef decltype(std::declval<__type34>()(std::declval<__type56>())) __type57;
    typedef decltype(std::declval<__type33>()(std::declval<__type57>())) __type58;
    typedef typename pythonic::lazy<__type58>::type __type59;
    typedef long __type61;
    typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type61>())) __type62;
    typedef typename pythonic::lazy<__type62>::type __type63;
    typedef typename __combined<__type59,__type63>::type __type64;
    typedef __type64 __type65;
    typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type61>())) __type67;
    typedef typename pythonic::lazy<__type67>::type __type68;
    typedef __type68 __type69;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type70;
    typedef pythonic::types::contiguous_slice __type74;
    typedef decltype(std::declval<__type23>()(std::declval<__type44>(), std::declval<__type50>(), std::declval<__type74>())) __type75;
    typedef typename pythonic::lazy<__type75>::type __type76;
    typedef __type76 __type77;
    typedef decltype(pythonic::operator_::mul(std::declval<__type61>(), std::declval<__type77>())) __type78;
    typedef typename pythonic::lazy<__type78>::type __type79;
    typedef typename __combined<__type76,__type79>::type __type80;
    typedef __type80 __type81;
    typedef decltype(std::declval<__type70>()(std::declval<__type81>())) __type82;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type82>::type::iterator>::value_type>::type __type83;
    typedef __type83 __type84;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type84>::type>::type __type85;
    typedef typename pythonic::lazy<__type85>::type __type86;
    typedef __type86 __type87;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type65>(), std::declval<__type69>(), std::declval<__type87>())) __type88;
    typedef indexable<__type88> __type89;
    typedef typename __combined<__type32,__type89>::type __type90;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type92;
    typedef __type92 __type93;
    typedef decltype(std::declval<__type93>()[std::declval<__type51>()]) __type97;
    typedef typename pythonic::assignable<__type97>::type __type98;
    typedef __type98 __type99;
    typedef typename pythonic::assignable<__type15>::type __type100;
    typedef __type100 __type101;
    typedef decltype(pythonic::operator_::div(std::declval<__type99>(), std::declval<__type101>())) __type102;
    typedef decltype(std::declval<__type33>()(std::declval<__type102>())) __type103;
    typedef typename pythonic::assignable<__type103>::type __type104;
    typedef __type104 __type105;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type65>(), std::declval<__type105>(), std::declval<__type87>())) __type113;
    typedef indexable<__type113> __type114;
    typedef typename __combined<__type90,__type114>::type __type115;
    typedef decltype(pythonic::operator_::add(std::declval<__type105>(), std::declval<__type61>())) __type118;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type65>(), std::declval<__type118>(), std::declval<__type87>())) __type120;
    typedef indexable<__type120> __type121;
    typedef typename __combined<__type115,__type121>::type __type122;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type84>::type>::type __type124;
    typedef typename pythonic::lazy<__type124>::type __type125;
    typedef __type125 __type126;
    typedef container<typename std::remove_reference<__type126>::type> __type127;
    typedef decltype(std::declval<__type18>()[std::declval<__type105>()]) __type131;
    typedef decltype(pythonic::operator_::sub(std::declval<__type99>(), std::declval<__type131>())) __type132;
    typedef decltype(pythonic::operator_::div(std::declval<__type132>(), std::declval<__type101>())) __type134;
    typedef typename pythonic::assignable<__type134>::type __type135;
    typedef __type135 __type136;
    typedef decltype(pythonic::operator_::sub(std::declval<__type61>(), std::declval<__type136>())) __type137;
    typedef typename pythonic::assignable<__type124>::type __type140;
    typedef __type140 __type141;
    typedef decltype(pythonic::operator_::mul(std::declval<__type137>(), std::declval<__type141>())) __type142;
    typedef container<typename std::remove_reference<__type142>::type> __type143;
    typedef decltype(pythonic::operator_::mul(std::declval<__type136>(), std::declval<__type141>())) __type146;
    typedef container<typename std::remove_reference<__type146>::type> __type147;
    typedef typename __combined<__type122,__type89,__type127,__type114,__type143,__type121,__type147>::type __type148;
    typedef typename pythonic::assignable<__type148>::type __type149;
    typedef typename pythonic::lazy<__type80>::type __type150;
    typedef typename pythonic::lazy<__type64>::type __type151;
    typedef decltype(pythonic::operator_::add(std::declval<__type27>(), std::declval<__type61>())) __type155;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type155>(), std::declval<__type61>())) __type156;
    typedef typename pythonic::assignable<__type156>::type __type157;
    typedef __type157 __type158;
    typedef decltype(std::declval<__type1>()(std::declval<__type12>(), std::declval<__type21>(), std::declval<__type158>())) __type159;
    typedef decltype(std::declval<__type0>()(std::declval<__type159>())) __type160;
    typedef typename pythonic::assignable<__type160>::type __type161;
    typedef __type148 __type162;
    typedef decltype(std::declval<__type162>()(std::declval<__type74>(), std::declval<__type74>(), std::declval<__type61>())) __type163;
    typedef container<typename std::remove_reference<__type163>::type> __type164;
    typedef decltype(std::declval<__type162>()(std::declval<__type74>(), std::declval<__type74>(), std::declval<__type74>())) __type166;
    typedef pythonic::types::slice __type168;
    typedef decltype(std::declval<__type162>()(std::declval<__type74>(), std::declval<__type74>(), std::declval<__type168>())) __type169;
    typedef decltype(pythonic::operator_::add(std::declval<__type166>(), std::declval<__type169>())) __type170;
    typedef container<typename std::remove_reference<__type170>::type> __type171;
    typedef typename __combined<__type161,__type164,__type171>::type __type172;
    typedef typename pythonic::assignable<__type172>::type __type173;
    typename pythonic::assignable_noescape<decltype(std::get<1>(khs))>::type deltakh = std::get<1>(khs);
    typename pythonic::assignable_noescape<decltype(std::get<1>(kzs))>::type deltakz = std::get<1>(kzs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(khs))>::type nkh = pythonic::builtins::functor::len{}(khs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(kzs))>::type nkz = pythonic::builtins::functor::len{}(kzs);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nk0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nk1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    typename pythonic::assignable_noescape<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nomega = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    __type149 spectrum_kzkhomega = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega), pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, field_k0k1omega));
    {
      long  __target139708399546080 = nk0;
      for (long  ik0=0L; ik0 < __target139708399546080; ik0 += 1L)
      {
        {
          long  __target139708405972320 = nk1;
          for (long  ik1=0L; ik1 < __target139708405972320; ik1 += 1L)
          {
            __type150 values = field_k0k1omega(ik0,ik1,pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None));
            if (pythonic::operator_::ne(KX[pythonic::types::make_tuple(ik0, ik1)], 0.0))
            {
              values = pythonic::operator_::mul(2L, values);
            }
            typename pythonic::assignable_noescape<decltype(KH[pythonic::types::make_tuple(ik0, ik1)])>::type kappa = KH[pythonic::types::make_tuple(ik0, ik1)];
            typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh)))>::type ikh = pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh));
            __type151 ikz = pythonic::builtins::functor::int_{}(pythonic::builtins::functor::round{}(pythonic::operator_::div(pythonic::builtins::functor::abs{}(KZ[pythonic::types::make_tuple(ik0, ik1)]), deltakz)));
            if (pythonic::operator_::ge(ikz, pythonic::operator_::sub(nkz, 1L)))
            {
              ikz = pythonic::operator_::sub(nkz, 1L);
            }
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
              typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh))>::type coef_share = pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh);
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
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L))>::type nomega_ = pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L);
    __type173 spectrum_onesided = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega_));
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L) = spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L);
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(1L,pythonic::builtins::None)) = pythonic::operator_::add(spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(1L,nomega_)), spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::slice(-1L,pythonic::operator_::neg(nomega_),-1L)));
    return pythonic::operator_::div(spectrum_onesided, pythonic::operator_::mul(deltakz, deltakh));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_spatiotemporal_spectra::__transonic__()());
inline
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_spectrum_kzkhomega0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& field_k0k1omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1omega, khs, kzs, KX, KZ, KH);
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
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_spectrum_kzkhomega1(pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>&& field_k0k1omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1omega, khs, kzs, KX, KZ, KH);
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
    
    char const* keywords[] = {"field_k0k1omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_spectrum_kzkhomega1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    
    char const* keywords[] = {"field_k0k1omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega1(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5])));
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
                               "compute_spectrum_kzkhomega", "\n""    - compute_spectrum_kzkhomega(float64[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_spectrum_kzkhomega",
    (PyCFunction)__pythran_wrapall_compute_spectrum_kzkhomega,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the kz-kh-omega spectrum.\n""\n""    Supported prototypes:\n""\n""    - compute_spectrum_kzkhomega(float64[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])"},
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
                                      "2022-02-04 12:30:17.510080",
                                      "64a594b0f2571653acbbbe86a4dde89d1753992c73b33a16356d7081954d4008");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif