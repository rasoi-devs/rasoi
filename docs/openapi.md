# Rasoi API

> Version 0.1.0

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/](#get) | Index |
| GET | [/recommendations](#getrecommendations) | Recommendations |
| GET | [/recipes/{id}](#getrecipesid) | Recipe Detail |
| GET | [/ingredients-search](#getingredients-search) | Ingredients Search |
| GET | [/recipes-search](#getrecipes-search) | Recipes Search |
| GET | [/recipes-from-ingredients](#getrecipes-from-ingredients) | Recipes From Ingredients |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| Ingredient | [#/components/schemas/Ingredient](#componentsschemasingredient) |  |
| Recipe | [#/components/schemas/Recipe](#componentsschemasrecipe) |  |
| Recommendation | [#/components/schemas/Recommendation](#componentsschemasrecommendation) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |

## Path Details

***

### [GET]/

- Summary  
Index

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/recommendations

- Summary  
Recommendations

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  title: string
  description: string
}[]
```

***

### [GET]/recipes/{id}

- Summary  
Recipe Detail

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  title: string
  full_ingredients?: string[]
  directions?: string[]
  link: string
  source: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/ingredients-search

- Summary  
Ingredients Search

#### Parameters(Query)

```ts
q: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  name: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/recipes-search

- Summary  
Recipes Search

#### Parameters(Query)

```ts
q: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  title: string
  full_ingredients?: string[]
  directions?: string[]
  link: string
  source: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/recipes-from-ingredients

- Summary  
Recipes From Ingredients

#### Parameters(Query)

```ts
q?: string[]
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  title: string
  full_ingredients?: string[]
  directions?: string[]
  link: string
  source: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/Ingredient

```ts
{
  name: string
}
```

### #/components/schemas/Recipe

```ts
{
  id: integer
  title: string
  full_ingredients?: string[]
  directions?: string[]
  link: string
  source: string
}
```

### #/components/schemas/Recommendation

```ts
{
  title: string
  description: string
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
