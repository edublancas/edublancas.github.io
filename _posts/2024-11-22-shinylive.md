---
layout: post
title: "Exporting Shiny apps with Shinylive"
comments: false
---

I was playing around with [Shinylive](https://posit-dev.github.io/r-shinylive/) but
encounter some issues when using it, here's the code that worked. It uses Docker
to make it reproducible.

Copy all the following files in the same directory:

## `app/app.R`

Some hello world app for testing. Note that this is under the `app/` directory, you must
create this file under an `app/` directory.

```R
library(shiny)

# Define UI
ui <- fluidPage(
    titlePanel("Hello World Shiny App"),
    
    sidebarLayout(
        sidebarPanel(
            textInput("name", "Enter your name:", "World")
        ),
        
        mainPanel(
            h3("Greeting:"),
            textOutput("greeting")
        )
    )
)

# Define server logic
server <- function(input, output) {
    output$greeting <- renderText({
        paste("Hello,", input$name, "!")
    })
}

# Run the application
shinyApp(ui = ui, server = server)
```

## `convert.R`

Simple script to convert the Shiny app to Shinylive.

```R
shinylive::export("/app", "site")
```

## `Dockerfile`

```Dockerfile
FROM r-base

# install OS requirements
RUN apt-get update && apt-get install -y \
    libarchive-dev libssl-dev libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# install R requirements
COPY install.R /_shinylive/install.R
RUN Rscript /_shinylive/install.R

# copy the converter script
COPY convert.R /_shinylive/convert.R

WORKDIR /_shinylive

ENTRYPOINT ["Rscript", "/_shinylive/convert.R"]
```

## Exporting to Shinylive

```sh
# build the docker image
docker build -t shinylive .

# export app.R
docker run -v $(pwd):/app shinylive
```

Once the `docker run` command finishes, you'll see a `site/` directory.

Then, you can run the exported app with any HTTP server. If you have R, you can use `httpuv`:

```sh
# install httpuv
Rscript -e 'install.packages("httpuv", repos="https://cran.rstudio.com")'

# run httpuv - and open the printed URL
Rscript -e 'httpuv::runStaticServer("site/")'
```

If you have a Python installation:

```sh
# open: http://localhost:8000
python -m http.server 8000 --directory site
```