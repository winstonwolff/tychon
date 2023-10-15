Thoughts on Tychon values and metadata for them

[ Shortcut — list of stories ]( https://app.shortcut.com/nitidbit/stories/space/unsaved )


TODO
====

* Apply Tychon to something
    - DSL or Macros for automated testing
    - DSL or Macros for asserting the shape of data (related to typing)
    - Replacement for SASS, that can also write unit tests for CSS.
    - DSL or Macros for generating html

Ideas
-----


### Automated Testing

func::add [a b]
    '''
    Returns the sum of `a` and `b`.

    >>> add(1 2)
    3

    >>> add(0 0)
    0
    '''
    a + b

import :: describe test from: tspec
describe 'add()':
    test 'returns the sum of arguments':
        expect(add(3 4)).to eq(7)


### HTML generation, a la JSX

import(render html body h1 div ul li from: tyhtml)

func:: MyComponent [explative product_name]
    div:: id:'MyComponent' class:['first' 'second']
        h1:: class:'foo' id:'blah'
            "This is my string"
        p:: class:"plain_paragraph"
            '''Ut dolor aliqua dolor dolor culpa aliqua minim non enim aliquip cillum veniam
            id.  Do ut in cillum laborum ut voluptate.  Sit duis in adipiscing lorem est in ad
            consequat aliquip laboris.'''

func:: MyPage [goods_for_sale]
    div:: id:"MyPage"
        goods_for_sale |> map(-> MyComponent('Buy now for a limited time only' %1))

main :: func :: [stdin stdout]
    skews = ['12113' '3342']
    render(MyPage)

